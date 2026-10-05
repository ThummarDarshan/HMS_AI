import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from decouple import config

logger = logging.getLogger(__name__)

STRICT_SYSTEM_PROMPT = """You are a medication information assistant inside a Hospital Management System.
Your job is to explain information strictly from verified medical documentation.

You MUST follow these rules:
1. Use retrieved medical documents as the primary source of truth.
2. Never invent medical facts.
3. Never invent medication names.
4. Never invent dosage.
5. Never invent contraindications.
6. Never invent drug interactions.
7. Never diagnose the patient.
8. Never independently prescribe medication.
9. Never claim certainty about a disease based only on symptoms.
10. If the retrieved documentation does not contain the answer, explicitly say:
    "I could not verify this information from the approved medication documentation."
11. Always cite official source information (CDSCO / DailyMed).
12. Explain official medication information in clear, patient-friendly language.
13. Clearly distinguish official-label information from general health guidance.
14. Always emphasize that medication selection requires clinical assessment by a qualified doctor.
15. If emergency symptoms are detected, prioritize urgent medical care.
16. Never fabricate citations.
"""


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        pass


class GeminiLLMProvider(BaseLLMProvider):
    """Google Gemini LLM Integration"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-flash"):
        self.api_key = api_key or config("GEMINI_API_KEY", default=config("LLM_API_KEY", default=""))
        self.model_name = config("GEMINI_MODEL", default=config("LLM_MODEL", default=model))

    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        if not self.api_key:
            return DeterministicRAGProvider().generate_chat_response(
                user_message, retrieved_context, patient_context
            )

        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)

            docs_text = "\n\n".join([
                f"### Medication: {doc.medication_name} ({doc.source})\n"
                f"Section: {doc.section_title}\n"
                f"Content: {doc.content}"
                for doc in retrieved_context.get("documents", [])
            ])

            prompt = (
                f"{STRICT_SYSTEM_PROMPT}\n\n"
                f"--- RETRIEVED OFFICIAL DOCUMENTATION ---\n"
                f"{docs_text if docs_text else 'NO VERIFIED DOCUMENTATION FOUND.'}\n\n"
                f"--- PATIENT QUERY ---\n{user_message}\n\n"
                f"Provide a structured, helpful explanation citing the verified sources."
            )

            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            logger.warning(f"Gemini API invocation fallback: {e}")
            return DeterministicRAGProvider().generate_chat_response(
                user_message, retrieved_context, patient_context
            )


class DeterministicRAGProvider(BaseLLMProvider):
    """
    Deterministic synthesis engine grounded strictly in retrieved documents.
    Operates 100% offline with zero external API dependencies and zero hallucination risk.
    """

    def generate_chat_response(
        self,
        user_message: str,
        retrieved_context: Dict[str, Any],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        medications = retrieved_context.get("medications", [])
        has_evidence = retrieved_context.get("has_verified_evidence", False)
        symptoms = retrieved_context.get("symptoms", [])

        if not has_evidence:
            return (
                "I could not verify this information from the approved medication documentation.\n\n"
                "To ensure your safety, I can only provide medical details that are grounded in verified regulatory sources "
                "(such as CDSCO or DailyMed). Please consult with your hospital physician or clinical specialist for guidance "
                "regarding these symptoms or specific medication needs."
            )

        response_parts = []

        if symptoms:
            response_parts.append(
                f"Based on your symptoms (**{', '.join([s.title() for s in symptoms])}**), "
                "here is verified information from official regulatory medication documentation. "
                "*Please note: this is informational and not a medical prescription.*"
            )
        else:
            response_parts.append(
                "Here is the verified information from official medication documentation:"
            )

        for med in medications:
            med_name = med.get("name", "Medication")
            sections = med.get("sections", {})
            brand_str = f" (Common brands: {', '.join(med['brand_names'][:3])})" if med.get("brand_names") else ""

            response_parts.append(f"\n### 💊 {med_name}{brand_str}")

            if "INDICATIONS" in sections:
                response_parts.append(f"**Approved Indications:**\n{sections['INDICATIONS']['content']}")

            if "DOSAGE_AND_ADMINISTRATION" in sections:
                response_parts.append(f"**Administration Guidance:**\n{sections['DOSAGE_AND_ADMINISTRATION']['content']}")

            if "WARNINGS" in sections:
                response_parts.append(f"⚠️ **Key Safety Warnings:**\n{sections['WARNINGS']['content']}")

            if "CONTRAINDICATIONS" in sections:
                response_parts.append(f"⛔ **Contraindications:**\n{sections['CONTRAINDICATIONS']['content']}")

            if "ADVERSE_REACTIONS" in sections:
                response_parts.append(f"ℹ️ **Possible Adverse Reactions / Side Effects:**\n{sections['ADVERSE_REACTIONS']['content']}")

            if "DRUG_INTERACTIONS" in sections:
                response_parts.append(f"🔄 **Known Drug Interactions:**\n{sections['DRUG_INTERACTIONS']['content']}")

            if "PATIENT_INFORMATION" in sections:
                response_parts.append(f"📋 **Patient Advice:**\n{sections['PATIENT_INFORMATION']['content']}")

        response_parts.append(
            "\n---\n"
            "👨‍⚕️ **Doctor Review Recommended:**\n"
            "Whether any medication is safe and appropriate for you depends on your personal health history, organ function, "
            "and other medications you may be taking. Please consult your doctor or schedule an appointment for clinical evaluation."
        )

        return "\n\n".join(response_parts)


def get_llm_provider() -> BaseLLMProvider:
    """Factory to return configured LLM provider"""
    provider_type = config("LLM_PROVIDER", default="auto").lower()
    gemini_key = config("GEMINI_API_KEY", default=config("LLM_API_KEY", default=None))

    if provider_type == "gemini" or (provider_type == "auto" and gemini_key):
        return GeminiLLMProvider(api_key=gemini_key)

    return DeterministicRAGProvider()
