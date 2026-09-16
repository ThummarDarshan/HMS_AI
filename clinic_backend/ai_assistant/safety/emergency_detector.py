import re
from typing import Dict, List, Any, Tuple


EMERGENCY_RED_FLAGS = [
    {
        "category": "Cardiac / Myocardial Infarction",
        "patterns": [
            r"\bchest pain\b",
            r"\bcrushing chest\b",
            r"\bpain radiating to (left arm|jaw|neck|back)\b",
            r"\bheart attack\b",
            r"\bsevere chest tightness\b",
            r"\bchest pressure\b",
        ],
        "reason": "Symptoms suggestive of acute coronary syndrome or myocardial ischemia.",
    },
    {
        "category": "Acute Respiratory Distress",
        "patterns": [
            r"\bcan('?t| not) breathe\b",
            r"\bsevere difficulty breathing\b",
            r"\bgasping for (air|breath)\b",
            r"\bsuffocating\b",
            r"\bchoking\b",
            r"\bturning blue\b",
            r"\bcyanosis\b",
            r"\bstridor\b",
        ],
        "reason": "Signs of severe airway compromise or acute respiratory failure.",
    },
    {
        "category": "Stroke / Neurological Emergency",
        "patterns": [
            r"\bface (droop|drooping)\b",
            r"\bsudden (numbness|paralysis|weakness) on one side\b",
            r"\bslurred speech\b",
            r"\bunable to speak\b",
            r"\bthunderclap headache\b",
            r"\bworst headache of my life\b",
            r"\bseizure\b",
            r"\bconvulsion\b",
        ],
        "reason": "Signs consistent with acute cerebrovascular accident (stroke) or intracranial pathology.",
    },
    {
        "category": "Severe Hemorrhage / Shock",
        "patterns": [
            r"\buncontrolled bleeding\b",
            r"\bsevere bleeding\b",
            r"\bvomiting (blood|coffee ground)\b",
            r"\bcoughing up blood\b",
            r"\bhemoptysis\b",
            r"\bloss of consciousness\b",
            r"\bpassed out\b",
            r"\bunresponsive\b",
            r"\bfainted\b",
        ],
        "reason": "Signs of hemodynamic instability or massive internal/external hemorrhage.",
    },
    {
        "category": "Severe Anaphylaxis",
        "patterns": [
            r"\bswelling of (throat|tongue|lips)\b",
            r"\bthroat closing\b",
            r"\banaphylaxis\b",
            r"\ballergic shock\b",
        ],
        "reason": "Acute systemic allergic reaction with imminent airway compromise.",
    },
    {
        "category": "Psychiatric Emergency / Self-Harm",
        "patterns": [
            r"\bsuicid(e|al)\b",
            r"\bkill myself\b",
            r"\bend my life\b",
            r"\bwant to die\b",
            r"\bself[- ]harm\b",
        ],
        "reason": "Acute psychiatric emergency or crisis situation requiring immediate intervention.",
    },
]


class EmergencyDetector:
    """
    Deterministic rule-based emergency & red-flag detector.
    Evaluates patient messages BEFORE any LLM call or medication recommendation.
    """

    @classmethod
    def evaluate(cls, user_text: str) -> Tuple[bool, List[Dict[str, str]], str]:
        """
        Returns:
            (is_emergency: bool, red_flags: List[Dict], emergency_guidance: str)
        """
        text_lower = user_text.lower().strip()
        detected_flags = []

        for flag_group in EMERGENCY_RED_FLAGS:
            for pattern in flag_group["patterns"]:
                if re.search(pattern, text_lower):
                    detected_flags.append({
                        "category": flag_group["category"],
                        "matched_term": pattern.replace(r"\b", ""),
                        "clinical_concern": flag_group["reason"],
                    })
                    break

        if detected_flags:
            emergency_message = (
                "🚨 **URGENT MEDICAL ATTENTION REQUIRED**\n\n"
                "Your message describes symptoms that may indicate a **critical medical emergency** "
                f"({', '.join([f['category'] for f in detected_flags])}).\n\n"
                "**Please take immediate action:**\n"
                "- **Call Emergency Medical Services (108 / 112 in India / 911)** immediately.\n"
                "- Go to the nearest Hospital Emergency Department right now.\n"
                "- Do NOT wait for an online chat or delay in-person emergency care.\n"
                "- If you are experiencing suicidal thoughts, contact the National Tele-MANAS helpline at **14416** or **1800 891 4416**."
            )
            return True, detected_flags, emergency_message

        return False, [], ""
