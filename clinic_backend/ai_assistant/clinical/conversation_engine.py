"""
Universal Clinical Conversation Engine
Manages stateful multi-turn clinical triage conversations:
- Dynamically selects ONE clinically relevant question at a time
- Adapts to previous patient answers without repeating questions
- Screens for emergency red flags at each turn
- Manages multi-symptom clusters seamlessly
- Produces structured, non-diagnostic clinical summaries with evidence-based guidance
- Handles follow-up questions within completed consultations
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple

from patients.models import Patient
from ai_assistant.clinical.condition_registry import (
    CONDITION_REGISTRY,
    get_condition_by_id,
    find_condition_by_text,
    find_all_conditions_by_text,
)
from ai_assistant.clinical.entity_extractor import ClinicalEntityExtractor
from ai_assistant.clinical.response_formatter import ClinicalResponseFormatter
from ai_assistant.safety.emergency_detector import EmergencyDetector

logger = logging.getLogger(__name__)


class UniversalClinicalEngine:
    """
    Core stateful clinical dialogue controller.
    """

    @classmethod
    def is_general_informational_query(cls, text: str) -> bool:
        """
        Determines if a query is a general informational inquiry, hospital navigation,
        or health FAQ rather than an active personal symptom complaint.
        """
        text_lower = text.lower().strip()

        # If user expresses personal suffering or self-reported physical distress
        personal_patterns = [
            r"\bi (have|got|am having|feel|am feeling|been having)\b",
            r"\bmy (head|stomach|throat|chest|back|belly|body|skin|eye) (hurts|aches|is hurting|pains)\b",
            r"\bi am suffering\b",
            r"\bstarted since\b",
            r"\bsince yesterday\b",
            r"\bwhat should i take for my\b",
        ]
        if any(re.search(pat, text_lower) for pat in personal_patterns):
            return False

        # Hospital administration, appointments, services
        hospital_services = [
            r"\bvisiting hour", r"\bappointment\b", r"\bopd\b", r"\bdoctor timing",
            r"\bbooking\b", r"\bbook doctor", r"\bhelpline\b", r"\badmission\b",
            r"\bdischarge\b", r"\bfirst aid\b", r"\bheimlich\b", r"\bcpr\b",
        ]
        if any(re.search(pat, text_lower) for pat in hospital_services):
            return True

        # Informational question openers
        info_openers = [
            r"^what (is|are|does|causes)",
            r"^how (can|do|to|does|is)",
            r"^can i drink",
            r"^can you explain",
            r"^tell me about",
            r"^what foods",
            r"^why do (people|we|i)",
            r"^is (walking|water|exercise|milk)",
            r"^information (on|about)",
        ]
        return any(re.search(pat, text_lower) for pat in info_openers)

    @classmethod
    def is_followup_query(cls, text: str, context: Dict[str, Any]) -> bool:
        """
        Detects if user is asking a follow-up question regarding an already-assessed condition
        (e.g. 'What can I do at home?', 'Is paracetamol safe?').
        """
        if not context.get("is_complete"):
            return False

        text_lower = text.lower().strip()
        followup_patterns = [
            r"what (can|should) i do (at home|now)",
            r"how (can|to) (treat|cure|manage|relieve)",
            r"is (paracetamol|ibuprofen|medicine|tablet|it) safe",
            r"can i take",
            r"should i (rest|drink|take)",
            r"what foods should i",
            r"how long will (it|this) last",
            r"when should i see",
            r"home remedies",
            r"side effects",
        ]
        return any(re.search(pat, text_lower) for pat in followup_patterns)

    @classmethod
    def evaluate_turn(
        cls,
        user_message: str,
        session_context: Optional[Dict[str, Any]] = None,
        patient: Optional[Patient] = None,
        chat_history: Optional[List[Any]] = None,
    ) -> Dict[str, Any]:
        """
        Executes one turn of the universal clinical conversation workflow:
        1. Emergency Red-Flag Screening
        2. Follow-up query detection on completed context
        3. Symptom & condition identification
        4. Patient context update & entity extraction
        5. Next ONE question selection (or completion summary)
        """
        context = dict(session_context or {})
        text_clean = user_message.strip()

        # Step 1: Emergency Red Flag Screening (HIGHEST PRIORITY)
        is_emergency, red_flags, emergency_guidance = EmergencyDetector.evaluate(text_clean)
        if is_emergency:
            context["is_emergency"] = True
            return {
                "answer": emergency_guidance,
                "intent": "EMERGENCY",
                "is_emergency": True,
                "red_flags": red_flags,
                "information_complete": True,
                "context": context,
                "symptoms": context.get("detected_symptoms", []),
                "medications": [],
                "sources": [],
            }

        # Step 2: Check if this is a follow-up on an already completed clinical consultation
        if cls.is_followup_query(text_clean, context):
            return cls._handle_followup(text_clean, context, patient)

        # Step 3: Check if this is an in-progress consultation
        condition_id = context.get("condition_id")
        condition_config = get_condition_by_id(condition_id) if condition_id else None

        if not condition_config:
            # New symptom detection
            matched_conditions = find_all_conditions_by_text(text_clean)
            if matched_conditions:
                condition_config = matched_conditions[0]
                condition_id = condition_config["condition"]
                context["condition_id"] = condition_id
                context["detected_symptoms"] = [c["displayName"] for c in matched_conditions]
                context["collected_data"] = {}
                context["asked_questions"] = []
                context["turn_count"] = 0
                context["is_complete"] = False
            else:
                # Fallback to general inquiry if no condition identified
                return {
                    "answer": None,  # Signals LLM to provide general guidance
                    "intent": "GENERAL_HEALTH",
                    "is_emergency": False,
                    "red_flags": [],
                    "information_complete": True,
                    "context": context,
                    "symptoms": [],
                    "medications": [],
                    "sources": [],
                }

        # Step 4: Extract entities from user message
        extracted = ClinicalEntityExtractor.extract_all_entities(text_clean, condition_config, patient)

        # If a question was previously asked, associate user's answer with that question
        last_question_id = context.get("last_question_id")
        collected_data = context.get("collected_data", {})

        # Map answer to last question if specifically waiting for it
        if last_question_id:
            if last_question_id == "age" and "age" in extracted:
                collected_data["age"] = extracted["age"]
            elif last_question_id == "duration" and "duration" in extracted:
                collected_data["duration"] = extracted["duration"]
            elif last_question_id == "temperature" and "temperature" in extracted:
                collected_data["temperature"] = extracted["temperature"]
            elif last_question_id in ["severity", "character_and_severity"] and "severity" in extracted:
                collected_data["severity"] = extracted["severity"]
            elif last_question_id == "onset" and "onset" in extracted:
                collected_data["onset"] = extracted["onset"]
            elif last_question_id in ["location", "location_and_duration"] and "location" in extracted:
                collected_data["location"] = extracted["location"]
            elif last_question_id in ["character", "sensation_character"] and "character" in extracted:
                collected_data["character"] = extracted["character"]
            elif last_question_id == "associated_symptoms":
                collected_data["associated_symptoms"] = extracted.get("associated_symptoms", {"raw": text_clean})
            else:
                # Store verbatim response for context
                collected_data[last_question_id] = text_clean

        # Also store all other extracted fields from this turn
        for k, v in extracted.items():
            if k not in collected_data:
                collected_data[k] = v

        # Check patient profile for age if still unknown
        if "age" not in collected_data:
            profile_age = ClinicalEntityExtractor.get_profile_age(patient)
            if profile_age:
                collected_data["age"] = profile_age

        context["collected_data"] = collected_data
        context["turn_count"] = context.get("turn_count", 0) + 1

        # Step 5: Determine next clinical question to ask (ONE QUESTION AT A TIME)
        # Step 5: Determine next clinical question to ask (ONE QUESTION AT A TIME)
        asked_questions = context.get("asked_questions", [])
        questions = condition_config.get("questions", [])

        next_question = None
        for q in questions:
            qid = q["id"]
            if qid in asked_questions:
                continue

            # Check if this question is already answered by extracted context
            if qid == "age" and "age" in collected_data:
                asked_questions.append("age")
                continue
            if qid == "duration" and "duration" in collected_data:
                asked_questions.append("duration")
                continue
            if qid == "duration_and_frequency" and "duration" in collected_data:
                asked_questions.append("duration_and_frequency")
                continue
            if qid == "temperature" and "temperature" in collected_data:
                asked_questions.append("temperature")
                continue
            if qid in ["severity", "character_and_severity"] and "severity" in collected_data:
                asked_questions.append(qid)
                continue
            if qid == "onset" and ("onset" in collected_data or ("duration" in collected_data and "severity" in collected_data and "associated_symptoms" in collected_data)):
                asked_questions.append("onset")
                continue
            if qid in ["location", "location_and_duration"] and "location" in collected_data:
                asked_questions.append(qid)
                continue
            if qid == "character" and "character" in collected_data:
                asked_questions.append("character")
                continue
            if qid == "associated_symptoms" and "associated_symptoms" in collected_data and context["turn_count"] > 1:
                asked_questions.append("associated_symptoms")
                continue

            # Selected next question
            next_question = q
            break

        # Step 6: If there is a next question, format and return it
        # Limit questioning to maximum 5 turns to avoid exhausting patient
        if next_question and context["turn_count"] <= 5:
            asked_questions.append(next_question["id"])
            context["asked_questions"] = asked_questions
            context["last_question_id"] = next_question["id"]
            context["is_complete"] = False

            # Empathetic acknowledgment for turns after Turn 1
            acknowledgments = ["Thanks.", "Thank you.", "Understood.", "Got it."]
            ack = acknowledgments[(context["turn_count"] - 1) % len(acknowledgments)]

            # Check for turn 1 prefix
            turn1_prefix = None
            if context["turn_count"] == 1:
                detected_syms = context.get("detected_symptoms", [])
                if len(detected_syms) > 1:
                    clean_sym_list = ", ".join(detected_syms[:-1]) + " and " + detected_syms[-1]
                    turn1_prefix = (
                        f"I'm sorry you're dealing with {clean_sym_list}. I can help you understand your symptoms and provide general health information.\n\n"
                        f"**First, {next_question['question']}**"
                    )
                elif next_question.get("first_turn_prefix"):
                    turn1_prefix = next_question.get("first_turn_prefix")
                else:
                    disp = condition_config.get("displayName", "your symptoms")
                    turn1_prefix = (
                        f"I'm sorry you are experiencing {disp.lower()}. I can help you understand your symptoms and provide general health information.\n\n"
                        f"**First, {next_question['question']}**"
                    )

            question_msg = ClinicalResponseFormatter.format_single_question(
                question_text=next_question["question"],
                turn_number=context["turn_count"],
                prefix=turn1_prefix,
                acknowledgment=ack,
            )

            return {
                "answer": question_msg,
                "intent": "SYMPTOM_CLARIFICATION",
                "is_emergency": False,
                "red_flags": [],
                "information_complete": False,
                "context": context,
                "symptoms": context.get("detected_symptoms", [condition_config["displayName"]]),
                "medications": [],
                "sources": [],
            }

        # Step 7: Information collection is COMPLETE -> Generate structured clinical summary
        context["is_complete"] = True
        context["last_question_id"] = None

        patient_ctx = {
            "age": collected_data.get("age"),
            "allergies": getattr(patient, "allergies", "") if patient else "",
        }

        extra_syms = [s for s in context.get("detected_symptoms", []) if s != condition_config["displayName"]]
        summary_msg = ClinicalResponseFormatter.format_clinical_summary(
            condition_config=condition_config,
            patient_context=patient_ctx,
            collected_data=collected_data,
            extra_symptoms=extra_syms,
        )

        # Build candidate sources & medications
        sources = condition_config.get("sources", [])
        medications = []
        med_info = condition_config.get("medication_info")
        if med_info:
            medications.append({
                "name": med_info["name"],
                "generic_name": med_info["name"].split("/")[0].strip(),
                "indications": med_info.get("general_use", ""),
                "warnings": [med_info.get("warnings", "")],
                "contraindications": [med_info.get("contraindications", "")],
            })

        return {
            "answer": summary_msg,
            "intent": "AI_CONSULTATION",
            "is_emergency": False,
            "red_flags": [],
            "information_complete": True,
            "context": context,
            "symptoms": context.get("detected_symptoms", [condition_config["displayName"]]),
            "medications": medications,
            "sources": sources,
        }

    @classmethod
    def _handle_followup(
        cls,
        text: str,
        context: Dict[str, Any],
        patient: Optional[Patient] = None,
    ) -> Dict[str, Any]:
        """
        Handles follow-up inquiries in a completed consultation without restarting the questionnaire.
        """
        cond_id = context.get("condition_id", "fever")
        config = get_condition_by_id(cond_id) or CONDITION_REGISTRY.get("fever", {})
        collected = context.get("collected_data", {})
        display_name = config.get("displayName", "your symptoms")
        text_lower = text.lower()

        # Follow-up: Medication safety (e.g. 'Is paracetamol safe?')
        if any(w in text_lower for w in ["paracetamol", "acetaminophen", "ibuprofen", "medicine", "safe"]):
            med_info = config.get("medication_info")
            if med_info:
                age = collected.get("age", "adult")
                answer = (
                    f"### Medication Guidance for {med_info['name']}\n\n"
                    f"In general, **{med_info['name']}** is commonly used for temporary relief of {display_name.lower()}.\n\n"
                    f"**Safety Considerations for Your Context:**\n"
                    f"- **Age factor:** Appropriate dosing depends strictly on age (context: {age} years) and body weight.\n"
                    f"- **Key safety warning:** {med_info.get('warnings')}\n"
                    f"- **Contraindications:** {med_info.get('contraindications')}\n"
                    f"- **Possible side effects:** {med_info.get('adverse_effects')}\n\n"
                    f"> **Important:** Do not take paracetamol if you have liver conditions or are taking other medicines with paracetamol. Consult a doctor or pharmacist for individualized dosing."
                )
            else:
                answer = (
                    f"For {display_name}, over-the-counter medications should always be used with caution. "
                    "Consult a doctor or pharmacist to confirm the safest medication given your medical history and age."
                )

        # Follow-up: Home self-care (e.g. 'What can I do at home?')
        elif any(w in text_lower for w in ["home", "do at home", "remedies", "self-care", "what to do"]):
            advice = config.get("general_advice", [])
            advice_md = "\n".join([f"- {a}" for a in advice])
            answer = (
                f"### Home Self-Care Recommendations for {display_name}\n\n"
                f"Based on your symptoms, here are safe, evidence-based measures you can take at home:\n\n"
                f"{advice_md}\n\n"
                f"**When to seek medical attention:** If your symptoms do not start improving or if any red flag warning signs develop, schedule a visit via [Book Appointment](/appointments/new)."
            )

        else:
            # General follow-up response tailored to the active condition
            answer = (
                f"Regarding **{display_name}**: Remember to prioritize rest and hydration. "
                "If your symptoms continue or worsen, please consult a physician. "
                "You can schedule a consultation with our hospital specialists anytime via [Book Appointment](/appointments/new)."
            )

        return {
            "answer": answer,
            "intent": "FOLLOW_UP_GUIDANCE",
            "is_emergency": False,
            "red_flags": [],
            "information_complete": True,
            "context": context,
            "symptoms": context.get("detected_symptoms", [display_name]),
            "medications": [],
            "sources": config.get("sources", []),
        }
