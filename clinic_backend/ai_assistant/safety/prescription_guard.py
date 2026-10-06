import re
from typing import Tuple, Dict, Any, List


PRESCRIPTION_INTENT_PATTERNS = [
    r"\bwhat (medicine|drug|tablet|pill|antibiotic) (should|can|do) i (take|use|have)\b",
    r"\bprescribe (me|for me)\b",
    r"\bgive me (a prescription|medicine|antibiotics)\b",
    r"\bwhich medicine is best for\b",
    r"\btell me what to take\b",
    r"\bcan i take (antibiotic|azithromycin|amoxicillin)\b",
    r"\bwhat dose should i take\b",
]

INJECTION_PATTERNS = [
    r"ignore (all|previous|prior) (instructions|rules|guidelines)",
    r"bypass (safety|medical|system)",
    r"you are now (a doctor|unrestricted|god mode|dan)",
    r"disregard (the rules|system prompt)",
]

PEDIATRIC_PATTERNS = [
    r"\b(?:dose|dosage|how much)\s+(?:for|to give)\s+(?:my\s+)?(?:child|baby|infant|kid|toddler|newborn|son|daughter)\b",
    r"\b(?:child|baby|infant|toddler|kid)\s+dose\b",
    r"\bpediatric\s+(?:dose|dosage)\b",
    r"\bexact dose of this medicine for my child\b",
]

EMERGENCY_MED_PATTERNS = [
    r"\b(?:chest pain|heart attack|can't breathe|difficulty breathing|stroke|bleeding severe).*(?:what (?:medicine|drug|tablet)|should i take|can i take)\b",
    r"\b(?:what (?:medicine|drug|tablet)|should i take|can i take).*(?:chest pain|heart attack|can't breathe|difficulty breathing|stroke|bleeding severe)\b",
]


class PrescriptionGuard:
    """
    Enforces anti-prescription, refusal behaviors, and prompt injection policies.
    Guarantees the system never acts as an autonomous prescribing physician.
    """

    @classmethod
    def is_prescription_request(cls, text: str) -> bool:
        text_lower = text.lower().strip()
        return any(re.search(pat, text_lower) for pat in PRESCRIPTION_INTENT_PATTERNS)

    @classmethod
    def detect_prompt_injection(cls, text: str) -> bool:
        text_lower = text.lower().strip()
        return any(re.search(pat, text_lower) for pat in INJECTION_PATTERNS)

    @classmethod
    def detect_pediatric_dosing(cls, text: str) -> Tuple[bool, str]:
        """Safety refusal for pediatric dosing requests without clinical confirmation"""
        text_lower = text.lower().strip()
        if any(re.search(pat, text_lower) for pat in PEDIATRIC_PATTERNS):
            refusal_msg = (
                "⚠️ **PEDIATRIC DOSING SAFETY NOTICE**\n\n"
                "I cannot provide exact medication dosages for children, infants, or toddlers.\n\n"
                "Pediatric dosing is highly sensitive and requires:\n"
                "- The child's exact **weight in kilograms** and chronological age\n"
                "- Medication brand, concentration, and formulation (e.g. mg/5mL syrup)\n"
                "- Clinical evaluation of renal and hepatic function\n\n"
                "**Action:** Please consult your pediatrician or hospital healthcare professional directly for confirmed pediatric dosing."
            )
            return True, refusal_msg
        return False, ""

    @classmethod
    def detect_emergency_medication_request(cls, text: str) -> Tuple[bool, str]:
        """Safety refusal when patient asks for pills while experiencing critical symptoms"""
        text_lower = text.lower().strip()
        if any(re.search(pat, text_lower) for pat in EMERGENCY_MED_PATTERNS):
            refusal_msg = (
                "🚨 **URGENT MEDICAL NOTICE: DO NOT DELAY FOR MEDICATION**\n\n"
                "You are describing symptoms (such as severe chest pain or breathing difficulty) that may represent a critical medical emergency.\n\n"
                "**Do NOT attempt to self-medicate or take home pills for acute chest pain or severe respiratory distress.** "
                "This requires immediate, hands-on clinical evaluation.\n\n"
                "**Action:** Please call **108 / 112** or go to the nearest Hospital Emergency Department immediately."
            )
            return True, refusal_msg
        return False, ""

    @classmethod
    def get_anti_prescription_disclaimer(cls) -> str:
        return (
            "⚠️ **Medication Prescribing Policy Notice**\n\n"
            "As an AI Health Assistant, I cannot diagnose medical conditions or prescribe medications. "
            "Medication selection, dosing, and duration must always be determined by a qualified physician "
            "based on an in-person or clinical telehealth examination, your medical history, and clinical lab investigations.\n\n"
            "Below is verified informational documentation regarding medications commonly associated with these symptoms, "
            "along with warnings and contraindications from official regulatory sources (CDSCO / DailyMed). "
            "Please consult your hospital doctor before starting, stopping, or altering any medication."
        )

