import re
import datetime
from typing import Dict, List, Any, Optional, Tuple
from patients.models import Patient
from ai_assistant.safety.medical_knowledge import (
    COMPREHENSIVE_DISEASE_PROTOCOLS,
    extract_clinical_state_attributes,
    expand_medical_abbreviations,
)


def get_patient_age(patient: Optional[Patient]) -> Optional[int]:
    """Calculate patient age from date of birth if present in HMS profile"""
    if patient and patient.date_of_birth:
        today = datetime.date.today()
        dob = patient.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return None


def get_patient_active_meds(patient: Optional[Patient]) -> List[str]:
    """Retrieve recent prescriptions from HMS patient record"""
    if not patient:
        return []
    meds = []
    try:
        for p in patient.prescriptions.all()[:5]:
            if p.medications:
                meds.append(p.medications.strip())
    except Exception:
        pass
    return meds


# Backward compatibility dictionary pointing to comprehensive protocols
SYMPTOM_PROTOCOLS = COMPREHENSIVE_DISEASE_PROTOCOLS


class ClinicalStateEngine:
    """
    Manages multi-turn conversation clinical state, adaptive clarification questioning,
    and differential consideration generation across all disease systems.
    """

    @classmethod
    def is_pure_monograph_query(cls, text: str) -> bool:
        """
        Distinguishes pure informational queries (e.g. 'What is paracetamol used for?')
        from personal symptom descriptions or treatment requests.
        """
        text_lower = text.lower().strip()

        # If user expresses personal symptoms, it's not pure informational
        personal_indicators = [
            r"\bi have\b", r"\bi am suffering\b", r"\bmy \w+\b", r"\bme\b",
            r"\bi am feeling\b", r"\bstarted since\b", r"\bwhat should i take\b",
            r"\bwhat medicine should i take\b", r"\bwhich medicine is good\b",
            r"\bcan i take\b", r"\bprescribe\b", r"\bi got\b", r"\bfor my\b"
        ]
        has_personal = any(re.search(pat, text_lower) for pat in personal_indicators)
        if has_personal:
            return False

        # General informational questions
        info_patterns = [
            r"^what is [a-zA-Z\s]+ used for\??$",
            r"^what are the (side effects|warnings|contraindications|uses|interactions) of [a-zA-Z\s]+\??$",
            r"^tell me about [a-zA-Z\s]+\??$",
            r"^information on [a-zA-Z\s]+\??$",
            r"^what does the (official|regulatory|cdsco|dailymed) documentation say about [a-zA-Z\s]+\??$",
        ]
        return any(re.search(pat, text_lower) for pat in info_patterns)

    @classmethod
    def evaluate_clinical_state(
        cls,
        current_message: str,
        chat_history: List[Any],
        patient: Optional[Patient] = None,
    ) -> Dict[str, Any]:
        """
        Synthesizes conversation history + current message + verified HMS patient profile
        into a structured clinical state across all disease categories.
        """
        # Aggregate all user text in this session
        all_user_messages = []
        for msg in chat_history:
            if hasattr(msg, "role") and msg.role == "user":
                all_user_messages.append(msg.content)
            elif isinstance(msg, dict) and msg.get("role") == "user":
                all_user_messages.append(msg.get("content", ""))

        if current_message not in all_user_messages:
            all_user_messages.append(current_message)

        full_conversation_text = " ".join(all_user_messages).lower()

        # 1. Expand Medical Terminology in user text
        _, expanded_abbrs = expand_medical_abbreviations(full_conversation_text)

        # 2. Extract Structured Clinical Attributes across all turns
        attrs = extract_clinical_state_attributes(full_conversation_text)

        # 3. Detect Disease / Symptom Protocols across all body systems
        detected_protocols = []
        for key, proto in COMPREHENSIVE_DISEASE_PROTOCOLS.items():
            if any(re.search(r"\b" + re.escape(kw) + r"\b", full_conversation_text) for kw in proto["keywords"]):
                detected_protocols.append((key, proto))

        # 4. Extract Patient Context from HMS Profile
        profile_age = get_patient_age(patient)
        profile_allergies = patient.allergies.strip() if (patient and patient.allergies) else ""
        profile_history = patient.medical_history.strip() if (patient and patient.medical_history) else ""
        profile_meds = get_patient_active_meds(patient)

        effective_age = profile_age or attrs.get("age")

        # 5. Determine whether key information is present
        has_duration = bool(attrs.get("duration"))
        has_severity = bool(attrs.get("severity")) or bool(attrs.get("temperature"))
        has_location = bool(attrs.get("location"))
        turns_count = len(all_user_messages)

        # Sufficient information check
        if not detected_protocols:
            is_complete = turns_count >= 1
        else:
            # Complete if either:
            # - 2+ turns and duration + severity/temperature are answered, OR
            # - 3+ turns of conversation
            if turns_count >= 2 and (has_duration and has_severity):
                is_complete = True
            elif turns_count >= 3:
                is_complete = True
            else:
                is_complete = False

        # Compile differential considerations from top protocols
        differentials = []
        if detected_protocols:
            for _, proto in detected_protocols[:2]:
                differentials.extend(proto.get("differentials", []))

        state = {
            "chiefComplaint": detected_protocols[0][1]["name"] if detected_protocols else "General Inquiry",
            "detectedProtocols": [p[0] for p in detected_protocols],
            "differentials": differentials[:5],
            "attributes": attrs,
            "expandedAbbreviations": expanded_abbrs,
            "age": effective_age,
            "hasProfileAge": profile_age is not None,
            "allergies": profile_allergies,
            "currentMedications": profile_meds,
            "medicalConditions": profile_history,
            "hasDuration": has_duration,
            "hasSeverity": has_severity,
            "hasLocation": has_location,
            "informationComplete": is_complete,
            "turnsCount": turns_count,
            "doctorReviewRequired": True,
        }

        return state

    @classmethod
    def generate_clarification_response(
        cls,
        state: Dict[str, Any],
        user_message: str,
    ) -> str:
        """
        Generates conversational, non-overwhelming follow-up questions (2-3 max)
        tailored to the specific complaint, with differential diagnostic considerations
        and without repeating already-answered questions.
        """
        protocols = state.get("detectedProtocols", [])
        attrs = state.get("attributes", {})
        has_age = state.get("age") is not None
        has_duration = state.get("hasDuration", False)
        has_severity = state.get("hasSeverity", False)
        has_location = state.get("hasLocation", False)
        complaint = state.get("chiefComplaint", "your symptoms")
        differentials = state.get("differentials", [])

        response_lines = [
            f"I understand you are experiencing **{complaint}**.\n"
        ]

        # Present possible conditions with appropriate uncertainty (Pillar 3)
        if differentials:
            response_lines.append("### 🩺 Differential Considerations:")
            response_lines.append("Based on the initial symptoms reported, possible causes to evaluate include:")
            for diff in differentials[:4]:
                response_lines.append(f"- **{diff}**")
            response_lines.append("*(Note: These are clinical considerations to discuss with a doctor, not a definitive diagnosis.)*\n")

        response_lines.append("To guide you safely and verify whether in-person care is needed, please help with a few missing details:")

        questions = []

        # 1. Ask age only if not in profile and not provided yet
        if not has_age:
            questions.append("How old are you? (Age is essential for safe medication and clinical assessment).")

        # 2. Specific questions from protocol, filtering out already answered items
        if protocols:
            proto_key = protocols[0]
            proto = COMPREHENSIVE_DISEASE_PROTOCOLS.get(proto_key)
            if proto:
                for q in proto.get("intake_questions", []):
                    # Skip duration question if duration already known
                    if has_duration and any(w in q.lower() for w in ["how long", "how many days", "how many hours", "when did"]):
                        continue
                    # Skip severity/temperature question if already known
                    if has_severity and any(w in q.lower() for w in ["temperature", "scale of 1 to 10", "severity"]):
                        continue
                    # Skip location question if already known
                    if has_location and any(w in q.lower() for w in ["where in", "where is", "where precisely"]):
                        continue

                    if len(questions) < 3:
                        questions.append(q)

        # 3. Fallbacks if questions still empty or insufficient
        if not has_duration and len(questions) < 3:
            questions.append("How long have you had these symptoms, and are they getting better or worse?")

        if not has_severity and len(questions) < 3:
            questions.append("On a scale of 1 to 10, how severe is the discomfort?")

        if len(questions) < 2:
            questions.append("Do you have any red-flag signs such as high fever, difficulty breathing, or severe weakness?")

        # Format questions cleanly
        for i, q in enumerate(questions[:3], 1):
            response_lines.append(f"**{i}.** {q}")

        # Incorporate patient history understanding if present (Pillar 8)
        med_conditions = state.get("medicalConditions")
        if med_conditions:
            response_lines.append(f"\n*Noted from your health record: History of {med_conditions}. We will take this into account for clinical safety.*")

        response_lines.append(
            "\n*Your answers ensure we evaluate red flags and recommend safe, regulatory-backed care.*"
        )

        return "\n".join(response_lines)

