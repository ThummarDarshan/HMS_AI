import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from decouple import config
from ai_assistant.safety.medical_knowledge import (
    COMPREHENSIVE_DISEASE_PROTOCOLS,
    LAB_TEST_REFERENCE_RANGES,
    MEDICAL_ABBREVIATIONS,
    parse_lab_reports_from_text,
    extract_clinical_state_attributes,
    expand_medical_abbreviations,
    classify_user_intent,
)
from ai_assistant.safety.prescription_guard import PrescriptionGuard

logger = logging.getLogger(__name__)

CLINICAL_CHATBOT_SYSTEM_PROMPT = """You are an intelligent, empathetic, and medically responsible Clinical AI Health Assistant for Velora Care Hospital Management System (HMS).
You assist patients consulting regarding symptoms, health conditions, lab reports, and medications across ALL medical disease categories.

You adhere strictly to the 13 Core Healthcare Conversational Pillars:

================================================================================
1. PATIENT INFORMATION COLLECTION (STRUCTURED INTAKE)
================================================================================
Collect basic information in a structured, non-repetitive way:
- Chief complaint & primary symptoms
- When symptoms started (onset) & duration
- Severity (1–10 scale) or temperature reading
- Frequency & progression (getting better, worse, or same)
- Previous medical conditions (diabetes, hypertension, asthma, etc.)
- Current medications & allergies
- Associated signs (nausea, shortness of breath, dizziness)

================================================================================
2. SYMPTOM UNDERSTANDING ACROSS ALL BODY SYSTEMS
================================================================================
Recognize symptoms and clinical groupings across all disease systems:
- Respiratory: Cough, fever, sore throat, runny nose, shortness of breath, chest congestion, wheezing
- Digestive: Abdominal pain, vomiting, diarrhea, nausea, constipation, acid reflux, heartburn
- Neurological: Headache, dizziness, vertigo, weakness, numbness, confusion
- Cardiovascular: Chest pressure, palpitations, racing heartbeat
- Musculoskeletal: Joint pain, knee pain, lower back pain, muscle spasms, stiffness
- Dermatological: Rash, itching, hives (urticaria), redness, blisters
- Genitourinary: Burning urination (dysuria), urinary frequency, flank pain
- Endocrine / Metabolic: High/low blood sugar, extreme thirst, shakiness
- General / Systemic: Fever, fatigue, body aches, chills

================================================================================
3. SYMPTOM → POSSIBLE CONDITIONS (DIFFERENTIAL CONSIDERATIONS)
================================================================================
Identify potential causes / differential considerations, but NEVER claim a definitive diagnosis.
Always express appropriate clinical uncertainty:
Example: "Based on fever, cough, and sore throat, possible considerations to discuss with a doctor include:
- Viral Upper Respiratory Infection (Common Cold)
- Influenza (Flu)
- COVID-19
- Acute Bronchitis
Note: These are differential considerations for clinical discussion, not a final diagnosis."

================================================================================
4. FOLLOW-UP QUESTION GENERATION (DYNAMIC & NEVER REPETITIVE)
================================================================================
Patient provides symptom → Identify missing information → Ask 2 to 3 concise, relevant follow-up questions.
CRITICAL RULE: Check conversation history first. NEVER ask questions that the patient has ALREADY answered (e.g., if duration or temperature is already provided, do NOT ask for duration or temperature again).

================================================================================
5. EMERGENCY & RED-FLAG DETECTION
================================================================================
Immediately screen for life-threatening emergencies:
- Severe crushing chest pain radiating to arm/jaw, shortness of breath
- Sudden face droop, one-sided weakness, slurred speech (Stroke / FAST)
- Sudden thunderclap headache, stiff neck with high fever
- Unconsciousness, seizures, severe bleeding, coughing/vomiting blood
- Anaphylaxis (swelling of lips/tongue/throat, inability to breathe)
- Severe self-harm or suicidal thoughts
ACTION: Advise immediate emergency care (Call 108 / 112 in India / 911) and going to the hospital emergency department. Do not provide home remedies for emergencies.

================================================================================
6. MEDICATION INFORMATION GROUNDING
================================================================================
Ground all medication advice in official CDSCO (Govt of India) and DailyMed / FDA documentation:
- Generic name & common brand names
- Pharmacological class & indication
- Safe OTC dosage, timing, and administration (take with water after meals)
- Common vs serious adverse effects
- Key warnings, contraindications, and drug interactions

================================================================================
7. ALLERGY CHECKING & CONFLICT DETECTION
================================================================================
Cross-check patient profile allergies and user-stated allergies against medications and cross-reactive classes:
- Penicillin allergy conflicts with Amoxicillin, Ampicillin, Augmentin
- NSAID allergy conflicts with Ibuprofen, Aspirin, Diclofenac
- Sulfa allergy conflicts with Septra / Bactrim
NEVER recommend an offending or cross-reactive drug. Prominently alert the patient.

================================================================================
8. PATIENT HISTORY UNDERSTANDING
================================================================================
Actively retrieve and incorporate the patient's verified medical history from their HMS profile:
- E.g., if patient has Diabetes and complains of dizziness: address potential hypoglycemia or dehydration.
- E.g., if patient has Hypertension: avoid decongestants that raise BP (pseudoephedrine) and NSAIDs that cause fluid retention.

================================================================================
9. MEDICAL REPORT UNDERSTANDING (LAB VALUE INTERPRETATION)
================================================================================
When user shares laboratory values (CBC, Hemoglobin, Blood Sugar, HbA1c, Creatinine, LFT, Lipid profile, etc.):
- Extract test name and numeric value
- Compare against clinical reference ranges
- Flag result clearly: [NORMAL], [ELEVATED / HIGH], or [LOW]
- Provide clinical significance and next steps (e.g., fasting confirmation, repeat testing)
- Explicitly instruct patient to share reports with their doctor for formal diagnostic correlation.

================================================================================
10. MEDICAL TERMINOLOGY & ABBREVIATION EXPANSION
================================================================================
Fluently understand and expand clinical shorthand:
BP (Blood Pressure), HR (Heart Rate), DM (Diabetes Mellitus), HTN (Hypertension),
SOB (Shortness of Breath), UTI (Urinary Tract Infection), GERD (Acid Reflux),
CBC (Complete Blood Count), FBS/PPBS (Fasting/Post-Prandial Blood Sugar), HbA1c, LFT, KFT.

================================================================================
11. INTENT CLASSIFICATION
================================================================================
Recognize the user's conversational intent:
- SYMPTOM_INQUIRY, MEDICATION_QUESTION, REPORT_QUESTION, ALLERGY_QUESTION,
  EMERGENCY, MEDICAL_HISTORY, APPOINTMENT, HOSPITAL_INFORMATION, GENERAL_HEALTH_QUESTION.

================================================================================
12. CONVERSATION STATE TRACKING
================================================================================
Maintain a structured mental state of the patient's case:
{
  "symptoms": [...],
  "duration": "...",
  "severity_or_temperature": "...",
  "location": "...",
  "allergies": [...],
  "medications": [...]
}
Update this state each turn and tailor replies without asking already answered details.

================================================================================
13. MEDICAL SAFETY & REFUSAL BEHAVIOR
================================================================================
Strictly refuse unsafe or out-of-scope clinical requests:
- Pediatric dosing: "I need information such as the child's exact age, weight in kilograms, and clinical context. Pediatric dosing must be confirmed by a pediatrician or doctor."
- Emergency medication requests: "Severe chest pain or acute breathlessness requires urgent emergency evaluation. Please seek immediate hospital emergency care rather than relying on a chatbot."
- Prescription drugs: Do not write prescriptions for Schedule H/X drugs (antibiotics, steroids, opioids). Direct patient to a licensed physician.
"""


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        pass


class GeminiLLMProvider(BaseLLMProvider):
    """Google Gemini LLM Integration with Multi-Turn Clinical Triage"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-3.5-flash"):
        self.api_key = api_key or config("GEMINI_API_KEY", default=config("LLM_API_KEY", default=""))
        self.model_name = config("GEMINI_MODEL", default=config("LLM_MODEL", default=model))

    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        if not self.api_key:
            return DeterministicRAGProvider().generate_chat_response(
                user_message, retrieved_context, patient_context, chat_history
            )

        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)

            # 1. Format verified official documentation
            docs = retrieved_context.get("documents", [])
            docs_text = ""
            if docs:
                docs_text = "\n\n".join([
                    f"### Medication: {doc.medication_name} ({doc.source})\n"
                    f"Section: {doc.section_title}\n"
                    f"Content: {doc.content}"
                    for doc in docs[:6]
                ])

            # 2. Format Patient Profile Context
            patient_info = patient_context or {}
            patient_profile_str = (
                f"- Name: {patient_info.get('full_name', 'Patient')}\n"
                f"- Age: {patient_info.get('age', 'Not recorded in profile')}\n"
                f"- Known Allergies: {patient_info.get('allergies', 'None reported')}\n"
                f"- Medical History: {patient_info.get('medical_history', 'None reported')}\n"
                f"- Current Medications: {', '.join(patient_info.get('current_medications', [])) or 'None reported'}"
            )

            # 3. Format Multi-Turn Chat History
            history_text = ""
            if chat_history:
                formatted_turns = []
                for turn in chat_history[-8:]:  # Include last 8 turns for complete context
                    role = "Patient" if turn.get("role") == "user" else "Assistant"
                    content = turn.get("content", "").strip()
                    if content:
                        formatted_turns.append(f"{role}: {content}")
                if formatted_turns:
                    history_text = "\n".join(formatted_turns)

            # 4. Build prompt
            prompt_parts = [
                CLINICAL_CHATBOT_SYSTEM_PROMPT,
                "\n--- PATIENT PROFILE ---",
                patient_profile_str,
            ]

            if docs_text:
                prompt_parts.extend([
                    "\n--- VERIFIED CDSCO & DAILYMED REGULATORY MONOGRAPHS ---",
                    docs_text,
                ])

            if history_text:
                prompt_parts.extend([
                    "\n--- PREVIOUS CONSULTATION HISTORY ---",
                    history_text,
                ])

            prompt_parts.extend([
                "\n--- CURRENT PATIENT MESSAGE ---",
                f"Patient: {user_message}",
                "\nClinical AI Assistant Response (follow the 3-step workflow):",
            ])

            full_prompt = "\n".join(prompt_parts)

            # Candidate models for high availability
            candidate_models = [self.model_name]
            if self.model_name != "gemini-3.5-flash":
                candidate_models.append("gemini-3.5-flash")
            if "gemini-3.5-flash-lite" not in candidate_models:
                candidate_models.append("gemini-3.5-flash-lite")

            last_err = None
            for model_to_try in candidate_models:
                try:
                    response = client.models.generate_content(
                        model=model_to_try,
                        contents=full_prompt,
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception as ex:
                    logger.warning(f"Gemini model '{model_to_try}' invocation failed: {ex}")
                    last_err = ex
                    continue

            logger.error(f"All Gemini models failed, falling back to deterministic RAG: {last_err}")
            return DeterministicRAGProvider().generate_chat_response(
                user_message, retrieved_context, patient_context, chat_history
            )

        except Exception as e:
            logger.warning(f"Gemini API invocation fallback: {e}")
            return DeterministicRAGProvider().generate_chat_response(
                user_message, retrieved_context, patient_context, chat_history
            )


class DeterministicRAGProvider(BaseLLMProvider):
    """
    Deterministic clinical synthesis engine grounded strictly in verified documents
    and comprehensive medical knowledge across all 13 healthcare conversation capabilities.
    Operates 100% offline with zero external API dependencies.
    """

    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        text_lower = user_message.lower().strip()
        all_user_text = " ".join([h.get("content", "") for h in (chat_history or []) if h.get("role") == "user"] + [user_message])

        # Pillar 13: Pediatric dosing refusal
        is_peds, peds_refusal = PrescriptionGuard.detect_pediatric_dosing(user_message)
        if is_peds:
            return peds_refusal

        # Pillar 13: Emergency medication request refusal
        is_emerg_req, emerg_refusal = PrescriptionGuard.detect_emergency_medication_request(user_message)
        if is_emerg_req:
            return emerg_refusal

        # Pillar 9: Lab Report Understanding
        lab_reports = parse_lab_reports_from_text(user_message)
        if lab_reports:
            lines = [
                "📋 **LABORATORY REPORT INTERPRETATION**\n",
                "I have analyzed the test values from your message against standard clinical reference ranges:\n"
            ]
            for r in lab_reports:
                badge = "🔴 HIGH" if r["flag"] == "HIGH" else ("🟡 LOW" if r["flag"] == "LOW" else "🟢 NORMAL")
                lines.append(f"- **{r['test_name']}**: `{r['value']} {r['unit']}` [{badge}] (Reference range: {r['reference_range']})")
                lines.append(f"  *Clinical Note:* {r['guidance']}")

            lines.append("\n⚠️ **Important Medical Advice:**")
            lines.append("Lab values must always be correlated with your clinical symptoms and physical examination. Please schedule a review with your hospital physician to discuss appropriate management.")
            return "\n".join(lines)

        # Pillar 7: Direct allergy inquiries (e.g. "Can I take amoxicillin?")
        patient_allergies = (patient_context.get("allergies", "") if patient_context else "").lower()
        if "amoxicillin" in text_lower and "penicillin" in patient_allergies:
            return (
                "🚨 **CRITICAL ALLERGY ALERT: DO NOT TAKE THIS MEDICATION**\n\n"
                "You asked about **Amoxicillin**, but your hospital medical record lists an allergy to **Penicillin**.\n\n"
                "**Clinical Risk:** Amoxicillin belongs to the penicillin class of beta-lactam antibiotics. "
                "Taking amoxicillin with a known penicillin allergy carries a severe risk of cross-reactivity and potentially life-threatening anaphylaxis.\n\n"
                "**Action:** Please consult your doctor for a safe alternative antibiotic (such as a macrolide) that does not cross-react."
            )

        # Pillar 10: Medical abbreviation expansion check
        _, expanded = expand_medical_abbreviations(user_message)

        # Pillar 2 & 3: Disease protocols & Differentials
        detected_protocols = []
        for key, proto in COMPREHENSIVE_DISEASE_PROTOCOLS.items():
            if any(re.search(r"\b" + re.escape(kw) + r"\b", all_user_text.lower()) for kw in proto["keywords"]):
                detected_protocols.append((key, proto))

        attrs = extract_clinical_state_attributes(all_user_text)
        has_duration = bool(attrs.get("duration"))
        has_severity = bool(attrs.get("severity")) or bool(attrs.get("temperature"))
        has_location = bool(attrs.get("location"))

        # Pillar 4 & 12: Missing information intake (Ask 2-3 questions without repeating answered ones)
        if detected_protocols and (not has_duration or not has_severity) and len(chat_history or []) <= 2:
            proto = detected_protocols[0][1]
            diffs = proto.get("differentials", [])

            lines = [
                f"I understand you are experiencing **{proto['name']}**.\n"
            ]

            if diffs:
                lines.append("### 🩺 Differential Considerations:")
                lines.append("Based on the initial symptoms reported, possible conditions to evaluate include:")
                for d in diffs[:3]:
                    lines.append(f"- **{d}**")
                lines.append("*(Note: These are differential considerations for clinical discussion, not a definitive diagnosis.)*\n")

            lines.append("To guide you safely, please help answer a few missing questions:")
            q_list = []
            for q in proto.get("intake_questions", []):
                if has_duration and any(w in q.lower() for w in ["how long", "how many days", "how many hours", "when did"]):
                    continue
                if has_severity and any(w in q.lower() for w in ["temperature", "scale of 1 to 10", "severity"]):
                    continue
                if has_location and any(w in q.lower() for w in ["where in", "where is", "where precisely"]):
                    continue
                q_list.append(q)

            if not has_duration and not any("how long" in q.lower() for q in q_list):
                q_list.append("How long have you had this problem, and is it getting better or worse?")

            for i, q in enumerate(q_list[:3], 1):
                lines.append(f"**{i}.** {q}")

            # Pillar 8: Patient history understanding
            med_hx = (patient_context.get("medical_history", "") if patient_context else "")
            if med_hx:
                lines.append(f"\n*Noted from your health record: History of {med_hx}. We will consider this for clinical safety.*")

            return "\n".join(lines)

        # Non-critical complete answer with OTC medication
        medications = retrieved_context.get("medications", [])
        has_evidence = retrieved_context.get("has_verified_evidence", False)
        symptoms = retrieved_context.get("symptoms", [])

        if not has_evidence and not medications:
            return (
                "🟢 **CLINICAL HEALTH GUIDANCE**\n\n"
                "I have recorded your symptoms and health context. To ensure complete safety, please note that "
                "personalized treatment decisions require clinical examination by a physician.\n\n"
                "**Recommended Action:**\n"
                "- If your symptoms persist beyond 48-72 hours or are accompanied by fever (>102°F) or breathlessness, "
                "please schedule a consultation with our hospital physicians through the Velora Care portal.\n"
                "- Ensure adequate hydration, rest, and monitor for any sudden changes."
            )

        response_parts = [
            "🟢 **CONDITION ASSESSMENT: MILD / NON-CRITICAL**\n\n"
            f"Based on your symptoms (**{', '.join([s.title() for s in symptoms]) if symptoms else 'reported concern'}**) and lack of critical red flags, "
            "here is verified over-the-counter guidance grounded in official CDSCO / DailyMed regulatory monographs:"
        ]

        # Pillar 8: Patient history integration
        med_hx = (patient_context.get("medical_history", "") if patient_context else "")
        if med_hx:
            response_parts.append(f"*Patient Clinical Context: Verified history of {med_hx}. Recommendations screened for safety.*")

        for med in medications:
            med_name = med.get("name", "Medication")
            sections = med.get("sections", {})
            brand_str = f" (Common brands: {', '.join(med['brand_names'][:3])})" if med.get("brand_names") else ""

            response_parts.append(f"\n### 💊 Recommended First-Line: {med_name}{brand_str}")

            if "DOSAGE_AND_ADMINISTRATION" in sections:
                response_parts.append(f"**Dosage & Administration:**\n{sections['DOSAGE_AND_ADMINISTRATION']['content']}")

            if "INDICATIONS" in sections:
                response_parts.append(f"📄 **Proof & Clinical Justification:**\n{sections['INDICATIONS']['content']}")

            if "WARNINGS" in sections:
                response_parts.append(f"⚠️ **Key Safety Precautions:**\n{sections['WARNINGS']['content']}")

            if "CONTRAINDICATIONS" in sections:
                response_parts.append(f"⛔ **Contraindications:**\n{sections['CONTRAINDICATIONS']['content']}")

        response_parts.append(
            "\n---\n"
            "👨‍⚕️ **When to Consult a Doctor:**\n"
            "If your symptoms worsen, or if discomfort persists past 48 to 72 hours without relief, "
            "stop taking over-the-counter medicine and schedule an in-person consultation with our hospital doctor."
        )

        return "\n\n".join(response_parts)


def get_llm_provider() -> BaseLLMProvider:
    """Factory to return configured LLM provider"""
    provider_type = config("LLM_PROVIDER", default="auto").lower()
    gemini_key = config("GEMINI_API_KEY", default=config("LLM_API_KEY", default=None))

    if provider_type == "gemini" or (provider_type == "auto" and gemini_key):
        return GeminiLLMProvider(api_key=gemini_key)

    return DeterministicRAGProvider()
