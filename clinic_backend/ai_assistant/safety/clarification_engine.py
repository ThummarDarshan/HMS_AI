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
        Distinguishes pure informational queries (e.g. 'What is paracetamol used for?',
        hospital services, first aid, condition overviews, health FAQs)
        from personal symptom descriptions requiring dynamic clarification.
        """
        text_lower = text.lower().strip()

        # If user expresses personal suffering or urgent self-symptom descriptions
        personal_indicators = [
            r"\bi have (severe|a|my)?\s*(fever|loose motion|diarrhea|vomiting|cough|stomach pain|diabetes|high blood pressure|hypertension|asthma|migraine|rash|chest pain)",
            r"\bi (have|got|am having|feel|am feeling|been having)\b",
            r"\bi am suffering (from)?",
            r"\bi am feeling (sick|dizzy|nauseous)",
            r"\bmy (stomach|head|throat|belly|chest|bp|blood pressure|sugar) (hurts|is hurting|pains|aches|is high|high)",
            r"\bstarted since\b",
            r"\bwhat should i take for my\b",
            r"\bwhich medicine is best for my\b",
        ]
        has_personal = any(re.search(pat, text_lower) for pat in personal_indicators)
        if has_personal:
            return False

        # Domain keywords for hospital services, first aid, and general health
        general_health_keywords = [
            r"\bvisiting hour", r"\bvisiting time", r"\bappointment", r"\bopd\b",
            r"\bhospital service", r"\bdoctor timing", r"\bbooking\b", r"\bbook doctor",
            r"\bfirst aid\b", r"\bburns?\b", r"\bbleeding\b", r"\bfainting\b", r"\bchoking\b",
            r"\bheimlich\b", r"\bcpr\b", r"\bseizure\b", r"\bfracture\b", r"\bsnake bite",
            r"\bdengue\b", r"\bmalaria\b", r"\btyphoid\b", r"\bdiabetes\b", r"\bhypertension\b",
            r"\bblood pressure\b", r"\basthma\b", r"\bgerd\b", r"\bacidity\b", r"\bgastritis\b",
            r"\bfood poisoning\b", r"\bkidney stone", r"\buti\b", r"\burinary infection",
            r"\bwater intake\b", r"\bhydration\b", r"\bdash diet\b", r"\bdiabetic diet\b",
            r"\bvaccin", r"\bsleep hygiene\b", r"\binsomnia\b", r"\bantibiotic stewardship\b",
            r"\bmedication storage\b", r"\bprenatal\b", r"\bpregnancy test", r"\bpathology\b",
            r"\blaboratory\b", r"\bradiology\b", r"\bx-ray\b", r"\bmri\b", r"\bct scan\b",
            r"\bpharmacy\b", r"\bcashless\b", r"\btpa\b", r"\binsurance\b", r"\badmission\b",
            r"\bdischarge\b", r"\bcheckup package", r"\bemergency\b", r"\bhelpline\b"
        ]
        if any(re.search(kw, text_lower) for kw in general_health_keywords):
            return True

        # General informational question patterns
        info_patterns = [
            r"^what (is|are|does)",
            r"^how (can|do|to|does|is)",
            r"^when (is|are|should|can)",
            r"^where (is|are|can)",
            r"^tell me about",
            r"^explain\b",
            r"^give (me )?(information|info|details) (about|on)",
            r"^information (about|on)",
            r"^can (i|you|we)",
            r"used for\??$",
            r"(side effects|warnings|contraindications|uses|interactions|dosage|benefits)",
            r"(symptoms of|causes of|treatment of|diagnosis of|tests for)",
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
        Generates conversational, single-question clarification strictly adhering to
        the ONE QUESTION AT A TIME clinical requirement.
        """
        protocols = state.get("detectedProtocols", [])
        has_age = state.get("age") is not None
        complaint = state.get("chiefComplaint", "your symptoms")

        # 1. Ask age only if NOT in profile and not provided yet
        if not has_age:
            return (
                f"I'm sorry you are experiencing {complaint}. I can help you understand your symptoms and provide general health information.\n\n"
                "**First, how old are you?**"
            )

        # 2. Ask the single next clinically relevant question
        if protocols:
            proto_key = protocols[0]
            proto = SYMPTOM_PROTOCOLS.get(proto_key)
            if proto and proto.get("questions"):
                return f"Thank you for clarifying. **{proto['questions'][0]}**"

        return "Thank you for clarifying. **How long have you had these symptoms?**"
