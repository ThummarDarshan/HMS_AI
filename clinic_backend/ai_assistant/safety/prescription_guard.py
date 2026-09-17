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


class PrescriptionGuard:
    """
    Enforces anti-prescription and prompt injection policies.
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
