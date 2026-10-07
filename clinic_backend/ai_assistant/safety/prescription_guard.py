import re
from typing import Tuple, Dict, Any, List


PRESCRIPTION_INTENT_PATTERNS = [
    r"\bwhat (medicine|drug|tablet|pill|antibiotic) (should|can|do) i (take|use|have)\b",
    r"\bwhat (dose|dosage) (should|do|can) i (take|have)\b",
    r"\bwhat (dose|dosage) of \w+ (should|do|can) i (take|have)\b",
    r"\bprescribe (me|for me|medicine|drugs?|tablets?|antibiotics?)\b",
    r"\b(can you|could you|please) prescribe\b",
    r"\bgive me (a prescription|medicine|antibiotics?)\b",
    r"\bwhich (medicine|drug|antibiotic) is best for\b",
    r"\btell me what (medicine|antibiotic) to take\b",
    r"\bcan i take (antibiotic|azithromycin|amoxicillin|ciprofloxacin|augmentin)\b",
    r"\bneed (an antibiotic|a prescription|antibiotics)\b",
    r"\bwrite (me )?a prescription\b",
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
            "⚠️ **Medication Safety Notice**\n\n"
            "I can provide general educational information about medications, but I cannot diagnose your condition or prescribe a personalized medication or dosage. "
            "Medication selection, dosing, and duration must always be determined by a qualified healthcare professional based on an in-person or clinical examination.\n\n"
            "Would you like help finding or booking an appointment with a hospital doctor? You can book directly via the [Book Appointment](/appointments/new) page."
        )
