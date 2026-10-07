"""
Clinical Entity Extractor
Extracts clinical attributes (age, duration, temperature, severity, onset,
location, characteristics, associated symptoms) from natural language inputs.
"""

import re
import datetime
from typing import Dict, Any, Optional, List
from patients.models import Patient


class ClinicalEntityExtractor:
    """
    Robust natural language clinical entity extractor.
    """

    @classmethod
    def get_profile_age(cls, patient: Optional[Patient]) -> Optional[int]:
        """Calculates patient age from hospital profile date of birth if present."""
        if patient and getattr(patient, "date_of_birth", None):
            today = datetime.date.today()
            dob = patient.date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return None

    @classmethod
    def extract_age(cls, text: str, patient: Optional[Patient] = None) -> Optional[int]:
        """
        Extracts patient age from user text or hospital profile.
        Carefully avoids false positives from durations ("2 days") or temps ("102F").
        """
        # 1. Profile takes precedence if explicitly recorded
        profile_age = cls.get_profile_age(patient)
        if profile_age is not None and profile_age > 0:
            return profile_age

        text_clean = text.strip().lower()

        # Direct single number response (e.g. "20", "25", "42")
        if re.fullmatch(r"^\d{1,2}$", text_clean):
            val = int(text_clean)
            if 1 <= val <= 115:
                return val

        # Natural language patterns
        patterns = [
            r"\b(?:i am|i'm|age is|age|my age is)\s*[:=]?\s*(\d{1,2})\b(?!\s*(?:days?|weeks?|months?|hours?|degree|°|f|c|times|stools))",
            r"\b(\d{1,2})\s*(?:years?\s*old|yrs?\s*old|yo|y/o|years?|yrs?)\b",
            r"^\s*(\d{1,2})\s*$",
        ]

        for pat in patterns:
            match = re.search(pat, text_clean)
            if match:
                try:
                    val = int(match.group(1))
                    if 1 <= val <= 115:
                        return val
                except ValueError:
                    pass

        return None

    @classmethod
    def extract_duration(cls, text: str) -> Optional[str]:
        """
        Extracts duration expressions (e.g. '2 days', 'since yesterday', 'a week').
        """
        text_clean = text.strip().lower()

        # Direct duration patterns
        patterns = [
            r"\b(?:for\s+)?(\d+\s*(?:days?|weeks?|months?|hours?|hrs?|d))\b",
            r"\b(?:since\s+)(yesterday|today|last night|morning|this morning|\d+\s*(?:days?|weeks?|hours?))\b",
            r"\b(yesterday|today morning|since yesterday|since morning|since last night)\b",
            r"\b(a\s*(?:week|few days|couple of days|day|month))\b",
            r"\b(\d+)\s*(?:d|days?)\s*(?:ago)?\b",
        ]

        for pat in patterns:
            match = re.search(pat, text_clean)
            if match:
                return match.group(0).strip()

        # Handle simple single responses like "2 days"
        if re.search(r"\b\d+\s*days?\b", text_clean):
            return re.search(r"\b\d+\s*days?\b", text_clean).group(0)

        return None

    @classmethod
    def extract_temperature(cls, text: str) -> Optional[str]:
        """
        Extracts body temperature readings (e.g. '102F', '102°F', '38.5 C', '100').
        """
        text_clean = text.strip().lower()

        # Explicit Fahrenheit or Celsius
        temp_match = re.search(r"\b(\d{2,3}(?:\.\d)?)\s*(?:°?\s*[fc]|degrees?(?:\s*[fc])?)\b", text_clean)
        if temp_match:
            return temp_match.group(0).strip().upper()

        # Bare number in typical body temp range (97 to 106 F, or 36 to 41 C)
        bare_match = re.search(r"\b(\d{2,3}(?:\.\d)?)\b", text_clean)
        if bare_match:
            try:
                num = float(bare_match.group(1))
                if 97.0 <= num <= 106.0:
                    return f"{num}°F"
                elif 36.0 <= num <= 42.0:
                    return f"{num}°C"
            except ValueError:
                pass

        if "don't know" in text_clean or "haven't measured" in text_clean or "not measured" in text_clean:
            return "Not measured"

        if "normal" in text_clean or "mild" in text_clean:
            return "Mild / unmeasured"

        return None

    @classmethod
    def extract_severity(cls, text: str) -> Optional[str]:
        """
        Extracts severity (numerical scale 1-10 or descriptive rating).
        """
        text_clean = text.strip().lower()

        # Number on 1-10 scale
        scale_match = re.search(r"\b(\d{1,2})\s*(?:out of 10|/10|scale of 10|on 10)?\b", text_clean)
        if scale_match:
            try:
                num = int(scale_match.group(1))
                if 1 <= num <= 10:
                    return f"{num}/10"
            except ValueError:
                pass

        # Qualitative descriptions
        if re.search(r"\b(unbearable|excruciating|worst|extremely severe)\b", text_clean):
            return "Severe (high intensity)"
        if re.search(r"\b(severe|very bad|intense|sharp|very painful)\b", text_clean):
            return "Severe"
        if re.search(r"\b(moderate|medium|somewhat bad|bearable)\b", text_clean):
            return "Moderate"
        if re.search(r"\b(mild|slight|little|not too bad|minor)\b", text_clean):
            return "Mild"

        return None

    @classmethod
    def extract_onset(cls, text: str) -> Optional[str]:
        """Extracts onset speed (sudden vs gradual)."""
        text_clean = text.strip().lower()
        if re.search(r"\b(sudden|suddenly|thunderclap|all at once|all of a sudden|acute)\b", text_clean):
            return "Sudden"
        if re.search(r"\b(gradual|gradually|slowly|over time|started slowly|developed slowly)\b", text_clean):
            return "Gradual"
        return None

    @classmethod
    def extract_location(cls, text: str, condition_id: str = "") -> Optional[str]:
        """Extracts anatomical location described by patient."""
        text_clean = text.strip().lower()

        locations = [
            ("lower right", "Lower right abdomen"),
            ("lower left", "Lower left abdomen"),
            ("upper right", "Upper right abdomen"),
            ("upper stomach", "Upper abdomen / epigastric"),
            ("upper belly", "Upper abdomen"),
            ("lower stomach", "Lower abdomen"),
            ("lower belly", "Lower abdomen"),
            ("all over", "Generalized / diffuse"),
            ("forehead", "Forehead / frontal"),
            ("temple", "Temples / bitemporal"),
            ("back of head", "Occipital / back of head"),
            ("one side", "Unilateral / one side"),
            ("lower back", "Lower back (lumbar)"),
            ("upper back", "Upper back (thoracic)"),
            ("neck", "Neck / cervical"),
            ("chest", "Chest wall"),
        ]

        for kw, desc in locations:
            if kw in text_clean:
                return desc

        return None

    @classmethod
    def extract_character(cls, text: str) -> Optional[str]:
        """Extracts symptom qualities (e.g. dry cough vs wet cough, throbbing vs dull)."""
        text_clean = text.strip().lower()

        if re.search(r"\b(dry|tickly|without phlegm)\b", text_clean):
            return "Dry cough"
        if re.search(r"\b(wet|phlegm|mucus|productive|sputum)\b", text_clean):
            return "Productive (with phlegm)"
        if re.search(r"\b(throbbing|pulsating|pounding)\b", text_clean):
            return "Throbbing"
        if re.search(r"\b(sharp|stabbing|piercing)\b", text_clean):
            return "Sharp"
        if re.search(r"\b(cramping|cramps|colicky)\b", text_clean):
            return "Cramping"
        if re.search(r"\b(burning|acidic|heartburn)\b", text_clean):
            return "Burning"
        if re.search(r"\b(dull|aching|heavy)\b", text_clean):
            return "Dull ache"
        if re.search(r"\b(vertigo|spinning|room is spinning)\b", text_clean):
            return "Vertigo (spinning)"
        if re.search(r"\b(lightheaded|faint|floating)\b", text_clean):
            return "Lightheadedness"

        return None

    @classmethod
    def extract_associated_symptoms(cls, text: str) -> Dict[str, Any]:
        """
        Extracts positive and negative affirmations of associated symptoms.
        e.g., 'no cough, mild headache' -> positive: ['headache'], negative: ['cough'].
        """
        text_clean = text.strip().lower()

        # Check for complete negative response
        negative_indicators = [
            r"^\s*no\s*$", r"^\s*none\s*$", r"^\s*no other symptoms?\s*$",
            r"^\s*nothing else\s*$", r"^\s*just\s+(?:the\s+)?\w+\s*$",
            r"^\s*only\s+(?:the\s+)?\w+\s*$"
        ]
        if any(re.search(pat, text_clean) for pat in negative_indicators):
            return {"has_none": True, "positives": [], "negatives": ["all other symptoms"]}

        symptom_terms = [
            "cough", "sore throat", "headache", "vomiting", "nausea", "diarrhea",
            "body aches", "rash", "difficulty breathing", "chest pain", "chills",
            "shivering", "runny nose", "stiff neck", "vision changes", "weakness",
            "dizziness", "blood in stool", "blood in vomit"
        ]

        positives = []
        negatives = []

        for term in symptom_terms:
            # Check for negated symptom (e.g. "no cough", "without vomiting", "haven't had diarrhea")
            neg_pat = r"\b(?:no|not|without|neither|nor|never|haven'?t had)\s+(?:\w+\s+){0,2}" + re.escape(term) + r"\b"
            pos_pat = r"\b" + re.escape(term) + r"\b"

            if re.search(neg_pat, text_clean):
                negatives.append(term)
            elif re.search(pos_pat, text_clean):
                positives.append(term)

        return {
            "has_none": len(positives) == 0 and len(negatives) > 0,
            "positives": positives,
            "negatives": negatives,
            "raw_text": text_clean,
        }

    @classmethod
    def extract_all_entities(
        cls,
        text: str,
        condition_config: Optional[Dict[str, Any]] = None,
        patient: Optional[Patient] = None,
    ) -> Dict[str, Any]:
        """
        Aggregates all extracted clinical entities from user response into a clean dictionary.
        """
        cond_id = condition_config.get("condition", "") if condition_config else ""

        age = cls.extract_age(text, patient)
        duration = cls.extract_duration(text)
        temp = cls.extract_temperature(text)
        severity = cls.extract_severity(text)
        onset = cls.extract_onset(text)
        location = cls.extract_location(text, cond_id)
        character = cls.extract_character(text)
        associated = cls.extract_associated_symptoms(text)

        entities: Dict[str, Any] = {}
        if age is not None:
            entities["age"] = age
        if duration is not None:
            entities["duration"] = duration
        if temp is not None:
            entities["temperature"] = temp
        if severity is not None:
            entities["severity"] = severity
        if onset is not None:
            entities["onset"] = onset
        if location is not None:
            entities["location"] = location
        if character is not None:
            entities["character"] = character
        if associated["positives"] or associated["negatives"] or associated["has_none"]:
            entities["associated_symptoms"] = associated

        return entities
