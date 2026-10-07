from typing import List, Dict, Any, Optional
from patients.models import Patient


CROSS_REACTIVITY_MAP = {
    "penicillin": ["amoxicillin", "ampicillin", "augmentin", "amoxyclav", "cloxacillin", "piperacillin", "penicillin"],
    "nsaid": ["ibuprofen", "aspirin", "diclofenac", "naproxen", "combiflam", "mefenamic acid", "ketorolac"],
    "aspirin": ["ibuprofen", "aspirin", "diclofenac", "naproxen", "combiflam"],
    "sulfa": ["sulfamethoxazole", "bactrim", "septra", "cotrimoxazole", "sulfasalazine"],
    "paracetamol": ["paracetamol", "acetaminophen", "dolo 650", "crocin", "calpol"],
    "macrolide": ["azithromycin", "erythromycin", "clarithromycin"],
}


class AllergyChecker:
    """
    Checks retrieved medication names and active ingredients against
    the authenticated patient's registered allergies in HMS.
    """

    @classmethod
    def check_patient_allergies(
        cls, patient: Optional[Patient], medication_names: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of high-visibility allergy conflict alerts.
        """
        if not patient or not patient.allergies:
            return []

        allergies_text = patient.allergies.lower()
        conflicts = []

        for med in medication_names:
            med_clean = med.lower().strip()

            # Direct match check
            if med_clean in allergies_text:
                conflicts.append({
                    "medication": med,
                    "matched_allergy": med,
                    "severity": "CRITICAL",
                    "warning": f"CRITICAL ALLERGY ALERT: You have a documented allergy to '{med}' in your hospital health record.",
                })
                continue

            # Cross-reactivity check
            for allergen_class, related_drugs in CROSS_REACTIVITY_MAP.items():
                if allergen_class in allergies_text:
                    if med_clean in related_drugs or any(rel in med_clean for rel in related_drugs):
                        conflicts.append({
                            "medication": med,
                            "matched_allergy": allergen_class,
                            "severity": "CRITICAL",
                            "warning": (
                                f"CRITICAL ALLERGY ALERT: Your profile lists an allergy to '{allergen_class}'. "
                                f"'{med}' belongs to or cross-reacts with this class. "
                                "Do NOT take this medication without explicit clearance from your doctor."
                            ),
                        })
                        break

        return conflicts
