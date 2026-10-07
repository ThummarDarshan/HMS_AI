"""
Clinical Response Formatter
Constructs structured, empathetic, evidence-based clinical guidance strictly adhering to
safety guidelines, non-diagnostic principles, structured medication monographs, and authoritative sources.
"""

from typing import Dict, Any, List, Optional


class ClinicalResponseFormatter:
    """
    Standardizes patient-facing clinical responses with rich Markdown formatting.
    """

    @classmethod
    def format_single_question(
        cls,
        question_text: str,
        turn_number: int = 1,
        prefix: Optional[str] = None,
        acknowledgment: Optional[str] = None,
    ) -> str:
        """
        Formats a clean, empathetic, single-question conversational response.
        Ensures NO multiple questions and NO monograph dumping.
        """
        if turn_number == 1:
            if prefix:
                return prefix
            return (
                "I'm sorry you're feeling unwell. I can help you understand your symptoms and provide general health information.\n\n"
                f"**First, {question_text}**"
            )

        ack_text = acknowledgment or "Thank you."
        return f"{ack_text} **{question_text}**"

    @classmethod
    def format_clinical_summary(
        cls,
        condition_config: Dict[str, Any],
        patient_context: Dict[str, Any],
        collected_data: Dict[str, Any],
        extra_symptoms: Optional[List[str]] = None,
    ) -> str:
        """
        Formats the final comprehensive, evidence-based clinical summary following Section 20 format:
        ### Summary
        ### What your symptoms may indicate
        ### Warning signs
        ### General self-care
        ### Medication information (only when appropriate)
        ### When to see a doctor
        ### Sources
        """
        display_name = condition_config.get("displayName", "your reported symptoms")
        age = collected_data.get("age") or patient_context.get("age")
        duration = collected_data.get("duration")
        temp = collected_data.get("temperature")
        severity = collected_data.get("severity")
        character = collected_data.get("character")
        location = collected_data.get("location")
        associated_dict = collected_data.get("associated_symptoms", {})
        pos_associated = associated_dict.get("positives", []) if isinstance(associated_dict, dict) else []

        if extra_symptoms:
            for s in extra_symptoms:
                if s not in pos_associated and s.lower() != display_name.lower():
                    pos_associated.append(s)

        # 1. ### Summary
        summary_parts = []
        if age:
            summary_parts.append(f"a {age}-year-old reporting **{display_name}**")
        else:
            summary_parts.append(f"**{display_name}**")

        if duration:
            summary_parts.append(f"lasting for {duration}")
        if temp:
            summary_parts.append(f"with recorded temperature of {temp}")
        if severity:
            summary_parts.append(f"rated as {severity}")
        if character:
            summary_parts.append(f"characterized as {character.lower()}")
        if location:
            summary_parts.append(f"located in {location.lower()}")

        summary_desc = ", ".join(summary_parts)
        if pos_associated:
            clean_assoc = ", ".join(pos_associated)
            summary_desc += f", accompanied by {clean_assoc}."
        else:
            summary_desc += "."

        summary_section = (
            "### Summary\n\n"
            f"You have provided details regarding {summary_desc} "
            "Based on the clinical information shared, here is an educational overview to help you understand your symptoms and manage your care safely."
        )

        # 2. ### What your symptoms may indicate
        causes = condition_config.get("possible_causes", [
            "Acute viral infection or seasonal illness",
            "Localized inflammatory response or physical strain",
            "General physiological reaction",
        ])
        causes_md = "\n".join([f"- **{c}**" for c in causes])
        indications_section = (
            "### What your symptoms may indicate\n\n"
            "Symptoms like yours can occur with several potential conditions, including:\n"
            f"{causes_md}\n\n"
            "*Important Note: This health information is for educational purposes only and cannot confirm a diagnosis. A qualified healthcare professional should evaluate you in person to determine the exact cause.*"
        )

        # 3. ### Warning signs
        red_flags = condition_config.get("red_flags", [
            "Sudden severe worsening of symptoms",
            "Difficulty breathing, shortness of breath, or chest pain",
            "Confusion, extreme dizziness, or loss of consciousness",
            "Persistent vomiting or inability to keep fluids down",
        ])
        red_flags_md = "\n".join([f"- {rf}" for rf in red_flags])
        warnings_section = (
            "### Warning signs\n\n"
            "Please monitor closely for the following 'red flag' symptoms, which require prompt urgent medical evaluation:\n"
            f"{red_flags_md}"
        )

        # 4. ### General self-care
        advice = condition_config.get("general_advice", [
            "Ensure adequate hydration by regularly sipping clean water or electrolyte fluids.",
            "Get sufficient physical rest to support your immune system's recovery.",
            "Monitor your temperature and symptoms closely for any new or evolving signs.",
        ])
        advice_md = "\n".join([f"- {a}" for a in advice])
        self_care_section = (
            "### General self-care\n\n"
            f"{advice_md}"
        )

        # 5. ### Medication information
        med_info = condition_config.get("medication_info")
        med_section = ""
        if med_info:
            med_name = med_info.get("name", "Over-the-Counter Analgesic / Antipyretic")
            general_use = med_info.get("general_use", "For temporary relief of mild discomfort or fever reduction.")
            warnings = med_info.get("warnings", "Do not exceed package dosing limits. Avoid alcohol.")
            contra = med_info.get("contraindications", "Known allergy or severe liver/kidney impairment.")
            adverse = med_info.get("adverse_effects", "Gastrointestinal upset, rare hypersensitivity reactions.")
            interactions = med_info.get("interactions", "Avoid taking with other medications sharing the same active ingredients.")

            med_section = (
                "### Medication information\n\n"
                f"**Medication:** {med_name}\n\n"
                f"**General use:**\n{general_use}\n\n"
                f"**Important warnings:**\n{warnings}\n\n"
                f"**Contraindications:**\n{contra}\n\n"
                f"**Possible adverse effects:**\n{adverse}\n\n"
                f"**Drug interactions:**\n{interactions}\n\n"
                "> **Safety Notice:** Medication suitability and dosing depend on age, medical history, other medicines, allergies, and pregnancy status. Consult a qualified healthcare professional or pharmacist before taking any medication."
            )

        # 6. ### When to see a doctor
        when_to_see = condition_config.get("when_to_see_doctor", [
            "If your symptoms do not begin improving within 2 to 3 days",
            "If you develop any of the warning signs listed above",
            "If your symptoms progressively worsen or interfere significantly with daily life",
        ])
        when_md = "\n".join([f"- {w}" for w in when_to_see])
        doctor_section = (
            "### When to see a doctor\n\n"
            "Schedule an in-person clinical evaluation:\n"
            f"{when_md}\n\n"
            "You can schedule a consultation with our hospital physicians directly through [Book Appointment](/appointments/new)."
        )

        # 7. ### Sources
        sources = condition_config.get("sources", [
            {"name": "CDSCO (Central Drugs Standard Control Organization), Govt of India", "url": "https://cdsco.gov.in"},
            {"name": "World Health Organization (WHO) Clinical Guidelines", "url": "https://www.who.int"},
            {"name": "National Health Portal of India", "url": "https://www.nhp.gov.in"},
        ])
        sources_md = "\n".join([f"- **[{s['name']}]({s['url']})**" for s in sources])
        sources_section = (
            "### Sources\n\n"
            f"{sources_md}\n\n"
            "*Disclaimer: This clinical information assistant provides evidence-based guidance for informational purposes and does not replace the professional diagnosis, judgment, or treatment of a qualified healthcare provider.*"
        )

        sections = [
            summary_section,
            indications_section,
            warnings_section,
            self_care_section,
        ]
        if med_section:
            sections.append(med_section)
        sections.append(doctor_section)
        sections.append(sources_section)

        return "\n\n".join(sections)
