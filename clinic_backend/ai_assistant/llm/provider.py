import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from decouple import config

logger = logging.getLogger(__name__)

CLINICAL_SYSTEM_PROMPT = """You are "Velora AI Care", the official AI Medical & Clinical Assistant inside the Hospital Management System (HMS).
Your purpose is to provide empathetic, highly structured, safe, and helpful medical guidance. You operate as a smart clinical assistant.

CORE INTERACTION & ROUTING DIRECTIVES:

1. DIRECT ANSWERS FOR ANY BASIC, GENERAL, OR LIFESTYLE QUESTION (ALWAYS GIVE DIRECT ANSWERS):
- When the user asks ANY basic question, definition, lifestyle query, medication rule, nutrition question, everyday health inquiry, or general curiosity:
  Examples:
  * "Can I drink milk after taking medicine?"
  * "How much water should I drink in a day?"
  * "What is normal blood pressure?"
  * "What is diabetes?" / "What causes dengue?" / "What is cholesterol?"
  * "How can I prevent acid reflux?"
  * "How much sleep is recommended?"
  * "What foods are high in iron?"
  * "Why do I get headaches when stressed?"
  * "Is walking 30 minutes a day enough for heart health?"
  * "What does a CBC blood test check?"
  * Greetings / Casual inquiries: "Hello", "Hi", "Who are you?", "How can you help me?"
- ALWAYS PROVIDE A DIRECT, THOROUGH, CLEAR, AND INFORMATIVE ANSWER IMMEDIATELY.
- DO NOT ask clarifying questions for basic or general questions. Provide the answer with structured bullet points, clear facts, and practical health tips.

2. ONE RELEVANT QUESTION AT A TIME (ONLY FOR ACTIVE PERSONAL SYMPTOM COMPLAINTS):
- When a patient explicitly reports an ACTIVE personal symptom or acute physical complaint (e.g., "I have a fever", "I have severe stomach pain", "My head hurts since yesterday", "I feel dizzy today", "I have a bad cough and sore throat"):
  * FIRST, express empathy in ONE brief, supportive sentence (e.g., "I am sorry to hear that you are dealing with a fever.").
  * SECOND, ask EXACTLY ONE single, clinically relevant follow-up question to gather essential triage context:
    - Step 1 (Duration): "How long have you had the fever?"
    - Step 2 (Severity / Temperature / Location): "What is your highest measured temperature, and how did you measure it?" or "Where exactly is the pain located, and is it mild, moderate, or severe?"
    - Step 3 (Associated Symptoms): "Are you experiencing any other symptoms, such as headache, cough, sore throat, vomiting, body aches, rash, or pain while urinating?"
    - Step 4 (Exposure / Context): "Have you recently traveled, had mosquito exposure, or been around anyone who was sick?"
  * STRICT PROHIBITION: NEVER ask multiple questions at once during triage. Never say: "What is your age, temperature, duration, and other symptoms?". Only ask the SINGLE next most useful question.
  * DO NOT OVER-QUESTION: Stop after 2 to 3 clarifying turns or once key dimensions are gathered.

3. STRUCTURED FINAL CLINICAL GUIDANCE (AFTER SYMPTOM TRIAGE):
When sufficient context has been gathered for a personal symptom complaint, conclude with this clean structure:

### What your symptoms may indicate
[Clear educational explanation of potential non-definitive causes. Never give an absolute diagnosis.]

### What you can do now
[Supportive self-care, hydration, rest, safe non-pharmacological comfort steps.]

### Watch for these warning signs
[Specific red flags requiring urgent medical care.]

### When to see a doctor
[Clear guidance on when to seek in-person clinical evaluation.]

*Medical Notice: This guidance is educational and does not constitute a clinical diagnosis. Always consult a qualified physician for personalized care.*

4. FIRST AID INQUIRIES (IMMEDIATE ACTIONABLE STEPS):
- For first aid questions (e.g., "What should I do for a minor burn?", "First aid for a nosebleed", "Someone fainted"):
  * Give immediate, concise, step-by-step instructions:
    ### Immediate first aid
    [1, 2, 3 numbered actionable steps]
    ### What to avoid
    [Crucial things NOT to do, e.g., never apply ice/butter to burns, never tilt head backward for nosebleeds]
    ### When to seek urgent medical care
    [Red flags requiring emergency room evaluation]

5. HOSPITAL MANAGEMENT SYSTEM (HMS) SERVICES & NAVIGATION:
- Connect the patient to existing hospital features:
  * Book Appointment: Guide them to the [Book Appointment](/appointments/new) page.
  * View Medical Records / Reports: Guide them to [My Lab Reports](/my-lab-reports) or [Medical Records](/medical-records).
  * Doctors & Specialists: Guide them to the [Doctors](/doctors) directory or [Departments](/departments).
  * Visiting Hours: General hospital visiting hours are 10:00 AM – 12:00 PM and 5:00 PM – 7:00 PM (Emergency 24/7).

6. PRESCRIPTION POLICY (STRICT ANTI-PRESCRIBING GUARD):
- NEVER prescribe medication, give personalized drug schedules, or tell a patient to take specific prescription antibiotics.
- If asked "What antibiotic should I take?", "Prescribe medicine", or "What dose should I take?":
  * Provide the Medication Safety Notice.
  * Explain the general drug class educationally.
  * Explain why antibiotics require clinical assessment, lab cultures, and a doctor's prescription.
  * Recommend scheduling a consultation with a hospital doctor at [Book Appointment](/appointments/new).

7. MEDICAL SAFETY & TONE:
- Never say "You definitely have X".
- Use phrases like: "Symptoms like yours can occur with...", "Possible causes include...", "Consider discussing this with a doctor."
- Maintain a warm, empathetic, professional, and reassuring tone.
"""


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self,
        user_message: str,
        chat_history: Optional[List[Any]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        pass


class GeminiLLMProvider(BaseLLMProvider):
    """
    Direct Google Gemini LLM Integration operating purely through the Gemini API Key.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or config("GEMINI_API_KEY", default=config("LLM_API_KEY", default="")).strip()
        configured_model = config("GEMINI_MODEL", default=config("LLM_MODEL", default="gemini-3.5-flash-lite")).strip()
        self.model_name = model or configured_model or "gemini-3.5-flash-lite"
        # Ordered list of supported models with verified availability
        self.fallback_models = [
            self.model_name,
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.8-flash",
            "gemini-3.7-flash",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
        ]
        # Deduplicate while preserving order
        self.fallback_models = list(dict.fromkeys(self.fallback_models))

    def generate_chat_response(
        self,
        user_message: str,
        chat_history: Optional[List[Any]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        if not self.api_key:
            return (
                "⚠️ **AI Assistant Configuration Notice**:\n\n"
                "The AI Chatbot operates directly through the Google Gemini API key, but no API key is currently configured.\n\n"
                "Please configure `GEMINI_API_KEY` in your backend `.env` configuration file to enable the AI Chatbot."
            )

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            # Build System Instruction with patient profile context
            system_instruction = CLINICAL_SYSTEM_PROMPT
            if patient_context:
                patient_info_lines = []
                if patient_context.get("full_name"):
                    patient_info_lines.append(f"- Patient Name: {patient_context['full_name']}")
                if patient_context.get("allergies"):
                    patient_info_lines.append(f"- Known Allergies: {patient_context['allergies']}")
                if patient_context.get("medical_history"):
                    patient_info_lines.append(f"- Medical History / Chronic Conditions: {patient_context['medical_history']}")
                if patient_context.get("age"):
                    patient_info_lines.append(f"- Age: {patient_context['age']}")
                if patient_context.get("gender"):
                    patient_info_lines.append(f"- Gender: {patient_context['gender']}")

                if patient_info_lines:
                    system_instruction += (
                        "\n\n--- CURRENT PATIENT PROFILE CONTEXT ---\n"
                        + "\n".join(patient_info_lines)
                        + "\nAlways take the above profile into consideration, especially known allergies and chronic conditions!\n"
                    )

            # Build multi-turn conversational contents
            contents = []
            if chat_history:
                # Limit to the last 14 messages for conversational context
                recent_history = chat_history[-14:]
                for msg in recent_history:
                    role = getattr(msg, "role", None) or (msg.get("role") if isinstance(msg, dict) else "user")
                    content = getattr(msg, "content", None) or (msg.get("content") if isinstance(msg, dict) else "")
                    if not content or not content.strip():
                        continue
                    # In Google GenAI, roles are 'user' and 'model'
                    genai_role = "model" if role in ["assistant", "model", "system"] else "user"
                    contents.append(
                        types.Content(
                            role=genai_role,
                            parts=[types.Part.from_text(text=content.strip())],
                        )
                    )

            # Append current user message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_message.strip())],
                )
            )

            last_error = None
            for model_candidate in self.fallback_models:
                try:
                    response = client.models.generate_content(
                        model=model_candidate,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.35,
                        ),
                    )
                    if response and response.text:
                        return response.text.strip()
                except Exception as model_err:
                    last_error = model_err
                    logger.warning(f"Gemini model '{model_candidate}' failed: {model_err}. Trying next candidate...")
                    continue

            # If all model candidates failed
            logger.error(f"All Gemini models failed. Last error: {last_error}")
            return "I'm temporarily unable to process your request. Please try again in a moment."

        except Exception as e:
            logger.error(f"Gemini API initialization or execution error: {e}", exc_info=True)
            return "I'm temporarily unable to process your request. Please try again in a moment."


def get_llm_provider() -> BaseLLMProvider:
    """Factory to return configured LLM provider directly using API Key"""
    gemini_key = config("GEMINI_API_KEY", default=config("LLM_API_KEY", default=""))
    return GeminiLLMProvider(api_key=gemini_key)
