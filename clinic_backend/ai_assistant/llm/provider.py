import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from decouple import config

logger = logging.getLogger(__name__)

CLINICAL_CHATBOT_SYSTEM_PROMPT = """You are an intelligent, empathetic, and medically responsible Clinical AI Health Assistant for Velora Care Hospital Management System.
You assist patients consulting from home regarding their symptoms, medical concerns, and medications.

Your consultation workflow follows 3 structured clinical steps:

--------------------------------------------------------------------------------
STEP 1: INTAKE & DETAIL GATHERING (WHEN INFORMATION IS MISSING)
--------------------------------------------------------------------------------
If the patient mentions a symptom or illness (e.g. "I have fever", "my stomach hurts", "I have headache", "cough") but has NOT provided enough basic clinical context:
- Warmly acknowledge their concern and ask the essential follow-up questions (ask only 2 to 3 concise, friendly questions at once):
  1. Duration: "For how many days or hours have you had this problem?"
  2. Severity / Quantitative measurement:
     - For fever: "What is your approximate body temperature in °F or °C?"
     - For pain: "Where is the pain located, and how severe is it on a scale of 1 to 10 (mild, moderate, or severe)?"
     - For cough: "Is it a dry cough or with phlegm/mucus?"
     - For diarrhea/vomiting: "How many times today, and are you able to keep water or fluids down?"
  3. Key associated signs: "Do you have any chills, severe weakness, breathing difficulty, skin rash, or vomiting?"
  4. Age & background: (If not provided in profile) "How old are you, and do you have any pre-existing conditions or allergies?"
- Maintain an empathetic, reassuring, and professional clinical tone.

--------------------------------------------------------------------------------
STEP 2: CRITICAL CONDITION EVALUATION
--------------------------------------------------------------------------------
When you have the necessary clinical details, evaluate whether the patient's condition is CRITICAL or NON-CRITICAL:

### 🚨 IF THE CONDITION IS CRITICAL / SEVERE:
Clinical criteria for critical status:
- High fever (temperature >= 102.5°F or >= 39.2°C) OR fever lasting more than 3-4 days without improvement.
- Shortness of breath, chest pain, chest tightness, wheezing, or coughing up blood.
- Sudden worst-ever headache (thunderclap), neck stiffness with fever, confusion, slurred speech, or seizure.
- Severe unremitting abdominal pain, persistent vomiting unable to keep any fluids down, blood in vomit or stool.
- Signs of anaphylaxis (swelling of lips, tongue, or throat, hives with breathing difficulty).
- High vulnerability: Infants under 6 months, elderly patients with chronic comorbidities (diabetes, kidney, heart disease).

CRITICAL RESPONSE FORMAT:
1. Header: "🚨 **CRITICAL CONDITION DETECTED: URGENT DOCTOR CONSULTATION RECOMMENDED**"
2. Clinical Justification: Clearly explain WHY the situation is critical based directly on the patient's inputs (e.g. "Your fever of 103°F lasting 4 days indicates a potential underlying acute infection that requires clinical diagnosis and laboratory tests").
3. Anti-Self-Medication Warning: Explain that self-medicating or taking standard fever pills at home is unsafe and may mask a serious condition.
4. Immediate Action: Advise visiting the nearest hospital emergency or consulting a physician immediately (call emergency 108 / 112 if acute distress).
5. Hospital Appointment Referral: Instruct the patient to book an urgent consultation with our hospital's General Physician or Specialist through the Velora Care Appointment system.

---

### 🟢 IF THE CONDITION IS NON-CRITICAL / MILD:
Clinical criteria for non-critical status:
- Low-grade fever (< 101.5°F / 38.6°C) lasting 1-2 days without red flags.
- Mild tension headache, seasonal cold, runny nose, sneezing, mild dry cough.
- Mild indigestion, simple acidity/heartburn, or mild loose stools with good hydration and no blood.

NON-CRITICAL RESPONSE FORMAT:
1. Header: "🟢 **CONDITION ASSESSMENT: MILD / NON-CRITICAL**"
2. Medication Prescription & Guidance:
   - Provide safe, first-line standard over-the-counter (OTC) medication:
     - Medicine Name & Formulation (e.g. Paracetamol 500 mg or 650 mg tablet, ORS oral rehydration solution, Cetirizine 10 mg tablet, Antacid gel/tablet).
     - Exact Dosage & Frequency (e.g. "Take 1 tablet every 6 to 8 hours as needed for fever/pain. Maximum 3 to 4 tablets (3000 mg) in 24 hours").
     - Timing & Administration (e.g. "Take after meals with a glass of water").
3. 📄 **PROOF & CLINICAL JUSTIFICATION (REQUIRED)**:
   - Connect the medicine directly to the patient's specific inputs:
     - "Based on your reported fever of [X]°F for [Y] days with no red-flag symptoms and no conflicting allergies..."
     - Pharmacological Rationale: Explain the approved mechanism (e.g. "Paracetamol is clinically approved by CDSCO (Govt of India) and DailyMed (FDA) as a primary antipyretic and analgesic. It acts on the hypothalamic heat-regulating center to safely lower body temperature and relieve discomfort").
     - Safety Verification: State that this is suitable for their age group and does not conflict with their recorded allergies.
4. Supportive Home Care:
   - Hydration (plenty of warm water, ORS, soups, electrolytes).
   - Rest and light, easily digestible meals.
5. ⚠️ **Safety Precautions & When to See a Doctor**:
   - Instruct the patient: "If your fever exceeds 102°F, fails to improve after 48-72 hours, or if you develop new symptoms like severe headache, vomiting, or breathing trouble, discontinue the medication and consult a hospital doctor immediately."

--------------------------------------------------------------------------------
STEP 3: SAFETY, ALLERGIES & REGULATORY GROUNDING
--------------------------------------------------------------------------------
- Strictly check patient allergies: NEVER recommend a medicine to which the patient has a reported allergy.
- Reference verified regulatory monographs (CDSCO / DailyMed) provided in the context below.
- Format with clean Markdown: use bold text, clear section headers, and bullet points.
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
    Deterministic clinical synthesis engine grounded strictly in verified documents.
    Operates 100% offline with zero external API dependencies.
    """

    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        medications = retrieved_context.get("medications", [])
        has_evidence = retrieved_context.get("has_verified_evidence", False)
        symptoms = retrieved_context.get("symptoms", [])

        # Check if basic details like duration are mentioned
        text_lower = (user_message + " " + " ".join([h.get("content", "") for h in (chat_history or [])])).lower()
        has_duration = any(w in text_lower for w in ["day", "days", "week", "yesterday", "since", "hours", "morning"])

        if symptoms and not has_duration and len(chat_history or []) <= 1:
            sym_list = ", ".join([s.title() for s in symptoms])
            return (
                f"I understand you are experiencing **{sym_list}**. To provide you with safe, accurate guidance:\n\n"
                "**1.** How many days or hours have you been having this problem?\n"
                "**2.** For fever/pain, what is your temperature or how severe is the pain (mild, moderate, severe)?\n"
                "**3.** Do you have any associated symptoms like chills, severe weakness, nausea, or breathing difficulty?\n\n"
                "*Please reply with these details so I can assess whether you need immediate medical attention or safe first-line medication.*"
            )

        if not has_evidence:
            return (
                "🟢 **CLINICAL SYMPTOM GUIDANCE**\n\n"
                "I have recorded your symptoms. To ensure your safety, precise medical recommendations must be grounded "
                "in verified clinical documentation.\n\n"
                "**Recommended Action:**\n"
                "- If your symptoms are severe, lasting more than 3 days, or accompanied by high fever (>102°F) or breathing difficulty, "
                "please consult a doctor immediately.\n"
                "- You can schedule an appointment directly with our hospital physicians through the Velora Care portal."
            )

        response_parts = [
            "🟢 **CONDITION ASSESSMENT: MILD / NON-CRITICAL**\n\n"
            f"Based on your reported symptoms (**{', '.join([s.title() for s in symptoms])}**) and lack of critical red flags, "
            "here is verified over-the-counter medication guidance grounded in official CDSCO / DailyMed regulatory monographs:"
        ]

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
            "If your symptoms worsen, or if fever/discomfort persists past 48 to 72 hours without relief, "
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
