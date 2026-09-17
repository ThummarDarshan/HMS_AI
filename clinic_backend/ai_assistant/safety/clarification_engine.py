import re
import datetime
from typing import Dict, List, Any, Optional, Tuple
from patients.models import Patient


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


# Specific Symptom Protocols
SYMPTOM_PROTOCOLS = {
    "diarrhea": {
        "keywords": ["diarrhea", "loose motion", "watery stool", "loose stools", "upset stomach", "frequent stool", "motions"],
        "name": "diarrhea / loose motions",
        "red_flag_terms": ["blood in stool", "black stool", "high fever", "unable to drink", "cannot keep fluids down", "dizzy", "extreme weakness"],
        "questions": [
            "How long have you had the loose motions, and approximately how many times have you passed stools today?",
            "Have you noticed any fever, vomiting, blood/black color in the stool, or severe stomach cramps?",
            "Are you able to drink water/fluids (like ORS or coconut water) without vomiting?",
        ],
        "antibiotic_warning": True,
    },
    "fever": {
        "keywords": ["fever", "high temperature", "chills", "feeling hot", "shivering"],
        "name": "fever",
        "red_flag_terms": ["stiff neck", "rash", "difficulty breathing", "confusion", "seizure", "vomiting repeatedly"],
        "questions": [
            "How many days have you had the fever, and do you know your approximate body temperature?",
            "Do you have any associated symptoms like severe headache, neck stiffness, skin rash, or difficulty breathing?",
            "Is the fever getting higher or accompanied by shivering/chills?",
        ],
    },
    "headache": {
        "keywords": ["headache", "head pain", "migraine", "throbbing head"],
        "name": "headache",
        "red_flag_terms": ["thunderclap", "worst headache", "sudden severe", "vision change", "slurred speech", "weakness", "stiff neck"],
        "questions": [
            "Did this headache start suddenly or develop gradually, and where is the pain located?",
            "Do you have any vision changes, nausea/vomiting, fever, neck stiffness, or weakness?",
            "How severe would you rate the pain (mild, moderate, or severe)?",
        ],
    },
    "cough": {
        "keywords": ["cough", "coughing", "cold", "runny nose", "sore throat", "congestion"],
        "name": "cough and cold",
        "red_flag_terms": ["coughing blood", "difficulty breathing", "chest pain", "shortness of breath", "wheezing"],
        "questions": [
            "How long have you had the cough, and is it a dry cough or with phlegm/mucus?",
            "Do you have any fever, chest discomfort, or difficulty breathing?",
        ],
    },
    "abdominal_pain": {
        "keywords": ["stomach pain", "abdominal pain", "tummy ache", "belly pain", "cramps in stomach"],
        "name": "abdominal pain",
        "red_flag_terms": ["severe sharp pain", "vomiting blood", "rigid abdomen", "high fever", "fainting"],
        "questions": [
            "Where in your abdomen is the pain located (upper, lower, right, left), and how long has it lasted?",
            "Is the pain sharp, cramping, or dull, and is it accompanied by vomiting, fever, or changes in bowel movements?",
        ],
    },
    "vomiting": {
        "keywords": ["vomiting", "throwing up", "nausea", "puking"],
        "name": "vomiting and nausea",
        "red_flag_terms": ["blood in vomit", "coffee ground vomit", "severe dizziness", "unable to keep fluids", "reduced urination"],
        "questions": [
            "How long have you been vomiting, and are you able to keep sips of water/electrolytes down?",
            "Do you have any severe abdominal pain, fever, or dizziness when standing?",
        ],
    },
    "skin_allergy": {
        "keywords": ["rash", "hives", "itching", "skin allergy", "red spots"],
        "name": "skin rash / allergy",
        "red_flag_terms": ["throat swelling", "lip swelling", "tongue swelling", "trouble breathing", "wheezing"],
        "questions": [
            "When did the rash or itching appear, and is it spreading across your body?",
            "Did you recently start any new medication, food, or skincare product?",
            "Are you experiencing any swelling of your lips, tongue, or throat, or difficulty breathing?",
        ],
    },
}


class ClinicalStateEngine:
    """
    Manages multi-turn conversation clinical state and adaptive clarification questioning.
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
        into a structured clinical state.
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

        # 1. Detect Chief Complaints / Symptoms
        detected_protocols = []
        for key, proto in SYMPTOM_PROTOCOLS.items():
            if any(re.search(r"\b" + re.escape(kw) + r"\b", full_conversation_text) for kw in proto["keywords"]):
                detected_protocols.append((key, proto))

        # 2. Extract Patient Context from HMS Profile
        profile_age = get_patient_age(patient)
        profile_allergies = patient.allergies.strip() if (patient and patient.allergies) else ""
        profile_history = patient.medical_history.strip() if (patient and patient.medical_history) else ""
        profile_meds = get_patient_active_meds(patient)

        # Check if age was stated in conversation if not in profile
        age_in_text = None
        age_match = re.search(r"\b(?:i am|age is|age|i'm)?\s*(\d{1,2})\s*(?:years? old|yrs?|yo)?\b", full_conversation_text)
        if age_match:
            try:
                age_in_text = int(age_match.group(1))
            except ValueError:
                pass

        effective_age = profile_age or age_in_text

        # 3. Check Duration / Severity
        has_duration = bool(re.search(r"\b(day|days|week|weeks|hour|hours|since|yesterday|today|morning|night|from)\b", full_conversation_text))
        has_severity = bool(re.search(r"\b(mild|moderate|severe|high|intense|unbearable|little|slightly|worse|better|same)\b", full_conversation_text))
        has_frequency = bool(re.search(r"\b(\d+\s*times|\d+\s*stools|\d+\s*episodes|frequently|constantly|few times)\b", full_conversation_text))

        # 4. Determine if Information is Sufficient
        turns_count = len(all_user_messages)
        is_complete = False

        if not detected_protocols:
            # General health question or simple query
            is_complete = turns_count >= 1
        else:
            # Need symptom details (duration, severity or frequency, and red flags answered)
            if turns_count >= 2 and (has_duration or has_frequency):
                is_complete = True
            elif turns_count >= 3:
                is_complete = True

        state = {
            "chiefComplaint": detected_protocols[0][1]["name"] if detected_protocols else "General Inquiry",
            "detectedProtocols": [p[0] for p in detected_protocols],
            "age": effective_age,
            "hasProfileAge": profile_age is not None,
            "allergies": profile_allergies,
            "currentMedications": profile_meds,
            "medicalConditions": profile_history,
            "hasDuration": has_duration,
            "hasSeverity": has_severity,
            "hasFrequency": has_frequency,
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
        tailored to the specific complaint and missing information.
        """
        protocols = state.get("detectedProtocols", [])
        has_age = state.get("age") is not None
        has_duration = state.get("hasDuration", False)
        complaint = state.get("chiefComplaint", "your symptoms")

        response_lines = [
            f"I can help you understand verified information regarding **{complaint}**, but before we discuss medication details, I need a little more context to ensure safety:\n"
        ]

        questions = []

        # 1. Ask age only if NOT in profile and not provided yet
        if not has_age:
            questions.append("How old are you? (Medication safety and dosing depend significantly on age).")

        # 2. Symptom specific questions
        if protocols:
            proto_key = protocols[0]
            proto = SYMPTOM_PROTOCOLS.get(proto_key)
            if proto:
                for q in proto["questions"]:
                    if len(questions) < 3:
                        questions.append(q)

        # 3. Fallback general questions if not specific
        if len(questions) < 2:
            if not has_duration:
                questions.append("When did your symptoms start, and are they getting better or worse?")
            questions.append("Are you currently experiencing any severe symptoms, fever, or inability to keep fluids down?")

        # Number and format questions cleanly
        for i, q in enumerate(questions[:3], 1):
            response_lines.append(f"**{i}.** {q}")

        response_lines.append(
            "\n*Your answers help provide accurate, evidence-backed information from approved regulatory documentation.*"
        )

        return "\n".join(response_lines)
