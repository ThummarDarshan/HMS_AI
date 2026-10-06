import re
from typing import List, Dict, Any, Optional
from patients.models import Patient


CROSS_REACTIVITY_MAP = {
    "penicillin": ["amoxicillin", "ampicillin", "augmentin", "amoxyclav", "cloxacillin", "piperacillin", "penicillin"],
    "nsaid": ["ibuprofen", "aspirin", "diclofenac", "naproxen", "combiflam", "mefenamic acid", "ketorolac"],
    "aspirin": ["ibuprofen", "aspirin", "diclofenac", "naproxen", "combiflam"],
    "sulfa": ["sulfamethoxazole", "bactrim", "septra", "cotrimoxazole", "sulfasalazine"],
    "paracetamol": ["paracetamol", "acetaminophen", "dolo 650", "crocin", "calpol"],
    "macrolide": ["azithromycin", "erythromycin", "clarithromycin"],
    "cephalosporin": ["cefixime", "cephalexin", "ceftriaxone", "cefuroxime"],
}

ALL_KNOWN_DRUGS = set()
for drugs in CROSS_REACTIVITY_MAP.values():
    ALL_KNOWN_DRUGS.update(drugs)


class AllergyChecker:
    """
    Checks medications against registered HMS patient profile allergies
    and user-disclosed allergies in conversation text.
    """

    @classmethod
    def extract_allergies_from_text(cls, text: str) -> List[str]:
        """Detect allergies mentioned in conversational text (e.g. 'allergic to penicillin')"""
        allergies = []
        text_lower = text.lower()
        patterns = [
            r"(?:allergic to|allergy to|allergic with|reaction to)\s+([a-zA-Z\s]+?)(?:[\.,;]|$|\s+and|\s+or)",
            r"([a-zA-Z]+)\s+allergy",
        ]
        for pat in patterns:
            for match in re.finditer(pat, text_lower):
                matched = match.group(1).strip()
                if len(matched) > 2 and matched not in ["food", "dust", "pollen", "everything", "any"]:
                    allergies.append(matched)
        return allergies

    @classmethod
    def extract_drugs_from_text(cls, text: str) -> List[str]:
        """Extract mentioned drug names from text"""
        text_lower = text.lower()
        found = []
        for drug in ALL_KNOWN_DRUGS:
            if re.search(r"\b" + re.escape(drug) + r"\b", text_lower):
                found.append(drug)
        return found

    @classmethod
    def check_patient_allergies(
        cls,
        patient: Optional[Patient],
        medication_names: List[str],
        conversation_text: str = "",
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of high-visibility allergy conflict alerts.
        """
        allergies_text = (patient.allergies.lower() if patient and patient.allergies else "")
        if conversation_text:
            text_allergies = cls.extract_allergies_from_text(conversation_text)
            if text_allergies:
                allergies_text = (allergies_text + " " + " ".join(text_allergies)).strip()

        if not allergies_text:
            return []

        # Combine passed med names and any drugs found in text
        all_meds = set(medication_names)
        if conversation_text:
            for d in cls.extract_drugs_from_text(conversation_text):
                all_meds.add(d)

        conflicts = []

        for med in all_meds:
            med_clean = med.lower().strip()

            # Direct match check
            if med_clean in allergies_text:
                conflicts.append({
                    "medication": med.title(),
                    "matched_allergy": med,
                    "severity": "CRITICAL",
                    "warning": f"CRITICAL ALLERGY ALERT: An active allergy to '{med}' is recorded in your profile or chat history. Do NOT take this medication.",
                })
                continue

            # Cross-reactivity check
            for allergen_class, related_drugs in CROSS_REACTIVITY_MAP.items():
                if allergen_class in allergies_text:
                    if med_clean in related_drugs or any(rel in med_clean for rel in related_drugs):
                        conflicts.append({
                            "medication": med.title(),
                            "matched_allergy": allergen_class.title(),
                            "severity": "CRITICAL",
                            "warning": (
                                f"CRITICAL ALLERGY ALERT: An allergy to '{allergen_class.title()}' is recorded. "
                                f"'{med.title()}' belongs to or cross-reacts with this class. "
                                "Do NOT take this medication without explicit clearance from your doctor."
                            ),
                        })
                        break

        return conflicts

