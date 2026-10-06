import logging
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from patients.models import Patient
from ai_assistant.models import MedicationDocument, ChatSession, ChatMessage
from ai_assistant.serializers import (
    MedicationDocumentSerializer,
    ChatSessionSerializer,
    ChatMessageSerializer,
)
from ai_assistant.retrieval.search import MedicationRetrievalEngine
from ai_assistant.safety.emergency_detector import EmergencyDetector
from ai_assistant.safety.allergy_checker import AllergyChecker
from ai_assistant.safety.prescription_guard import PrescriptionGuard
from ai_assistant.safety.clarification_engine import (
    ClinicalStateEngine,
    get_patient_age,
    get_patient_active_meds,
)
from ai_assistant.safety.medical_knowledge import (
    classify_user_intent,
    parse_lab_reports_from_text,
    expand_medical_abbreviations,
    COMPREHENSIVE_DISEASE_PROTOCOLS,
)
from ai_assistant.llm.provider import get_llm_provider
from ai_assistant.ingestion.pipeline import MedicationIngestionPipeline

logger = logging.getLogger(__name__)


def get_or_create_patient_for_user(user) -> Patient:
    """Safely obtain or initialize patient record for authenticated user"""
    patient = Patient.objects.filter(user=user).first()
    if patient:
        return patient
    patient, _ = Patient.objects.get_or_create(user=user)
    return patient


class PatientChatAPIView(APIView):
    """
    Core AI Health & Medication Assistant Chat API.
    Enforces dynamic clarification questioning, emergency screening,
    patient allergy conflict checking, anti-prescription guardrails,
    and authoritative CDSCO/DailyMed RAG retrieval.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        patient = get_or_create_patient_for_user(user)

        message_text = request.data.get("message", "").strip()
        session_id = request.data.get("session_id")

        if not message_text:
            return Response(
                {"error": "Message content cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(message_text) > 2000:
            return Response(
                {"error": "Message is too long. Please limit your query to 2000 characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Resolve or create chat session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id, patient=patient)
            except ChatSession.DoesNotExist:
                return Response(
                    {"error": "Chat session not found or you are not authorized to access it."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            title = message_text[:40] + ("..." if len(message_text) > 40 else "")
            session = ChatSession.objects.create(patient=patient, title=title)

        past_messages = list(session.messages.all())

        # 2. Record User Message
        user_msg = ChatMessage.objects.create(
            session=session,
            role="user",
            content=message_text,
        )

        # 3. Step 1: Emergency Red Flag Screening (Always First)
        is_emergency, red_flags, emergency_guidance = EmergencyDetector.evaluate(message_text)
        is_emerg_med, emerg_med_guidance = PrescriptionGuard.detect_emergency_medication_request(message_text)
        if is_emergency or is_emerg_med:
            guidance = emergency_guidance or emerg_med_guidance
            flags = red_flags or [{"category": "Acute Emergency", "matched_term": "Critical Request", "clinical_concern": "Acute distress"}]
            assistant_msg = ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=guidance,
                intent="EMERGENCY",
                red_flags=flags,
                doctor_review_required=True,
                is_emergency=True,
            )
            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "EMERGENCY",
                "answer": guidance,
                "symptoms": [],
                "medications": [],
                "sources": [],
                "redFlags": flags,
                "allergyConflicts": [],
                "labReports": [],
                "differentials": [],
                "clinicalState": {},
                "abbreviationsExpanded": [],
                "doctorReviewRequired": True,
                "emergency": True,
                "informationComplete": False,
            })

        # Step 1b: Pediatric Dosing Safety Refusal
        is_peds, peds_guidance = PrescriptionGuard.detect_pediatric_dosing(message_text)
        if is_peds:
            assistant_msg = ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=peds_guidance,
                intent="PEDIATRIC_REFUSAL",
                red_flags=[],
                doctor_review_required=True,
                is_emergency=False,
            )
            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "PEDIATRIC_REFUSAL",
                "answer": peds_guidance,
                "symptoms": [],
                "medications": [],
                "sources": [],
                "redFlags": [],
                "allergyConflicts": [],
                "labReports": [],
                "differentials": [],
                "clinicalState": {},
                "abbreviationsExpanded": [],
                "doctorReviewRequired": True,
                "emergency": False,
                "informationComplete": False,
            })

        # 4. Medical Terminology & Abbreviation Expansion
        _, expanded_abbrs = expand_medical_abbreviations(message_text)

        # 5. Medical Laboratory Report Understanding
        lab_reports = parse_lab_reports_from_text(message_text)

        # 6. Clinical State Evaluation Across Multi-Turn History
        clinical_state = ClinicalStateEngine.evaluate_clinical_state(message_text, past_messages, patient)

        # 7. Intent Classification
        classified_intent = classify_user_intent(message_text)

        # 8. Grounded Document Retrieval across full conversation context
        all_conversation_text = " ".join([m.content for m in past_messages] + [message_text])
        retrieved = MedicationRetrievalEngine.retrieve(all_conversation_text)
        medications_data = retrieved.get("medications", [])
        sources = retrieved.get("sources", [])
        symptoms = retrieved.get("symptoms", [])

        # 9. Patient Profile & Conversation Allergy Conflict Check
        med_names_to_check = [m["name"] for m in medications_data] + [m.get("generic_name", "") for m in medications_data]
        allergy_conflicts = AllergyChecker.check_patient_allergies(patient, med_names_to_check, conversation_text=all_conversation_text)

        # 10. Patient Clinical Profile Context
        full_name = getattr(user, "full_name", None) or f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip() or getattr(user, "email", "Patient")
        patient_ctx = {
            "full_name": full_name,
            "age": get_patient_age(patient),
            "allergies": getattr(patient, "allergies", "") or "",
            "medical_history": getattr(patient, "medical_history", "") or "",
            "current_medications": get_patient_active_meds(patient),
        }

        # 11. Format Chat History for Multi-Turn Reasoning
        history_list = [
            {"role": m.role, "content": m.content}
            for m in past_messages
        ]

        # 12. Generate Intelligent Clinical Response via Provider
        llm = get_llm_provider()
        answer = llm.generate_chat_response(
            user_message=message_text,
            retrieved_context=retrieved,
            patient_context=patient_ctx,
            chat_history=history_list,
        )

        # 13. Classify Response State
        is_critical = bool(
            "CRITICAL" in answer.upper()
            or "URGENT MEDICAL ATTENTION" in answer.upper()
        )
        is_clarification = bool(
            not is_critical
            and "?" in answer
            and (
                "how many" in answer.lower()
                or "how long" in answer.lower()
                or "temperature" in answer.lower()
                or "what is your" in answer.lower()
                or "where is" in answer.lower()
            )
        )

        final_intent = classified_intent
        if is_critical:
            final_intent = "CRITICAL_ALERT"
        elif is_clarification:
            final_intent = "SYMPTOM_CLARIFICATION"

        # Show medication cards if safe OTC guidance is provided
        show_medications = medications_data if (not is_critical and not is_clarification) else []

        # 14. Store Assistant Response in Session History
        assistant_msg = ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer,
            intent=final_intent,
            symptoms=symptoms,
            medications_data=show_medications,
            sources=sources,
            red_flags=[],
            doctor_review_required=True,
            is_emergency=False,
        )
        session.save()

        return Response({
            "success": True,
            "session_id": str(session.id),
            "intent": final_intent,
            "answer": answer,
            "symptoms": symptoms,
            "medications": show_medications,
            "sources": sources,
            "redFlags": [],
            "allergyConflicts": allergy_conflicts,
            "labReports": lab_reports,
            "differentials": clinical_state.get("differentials", []),
            "clinicalState": clinical_state.get("attributes", {}),
            "abbreviationsExpanded": expanded_abbrs,
            "doctorReviewRequired": True,
            "emergency": False,
            "isCritical": is_critical,
            "informationComplete": clinical_state.get("informationComplete", not is_clarification),
        })


class ChatSessionListView(APIView):
    """List all sessions or create a new session for current authenticated patient"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        patient = get_or_create_patient_for_user(request.user)
        sessions = ChatSession.objects.filter(patient=patient)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        patient = get_or_create_patient_for_user(request.user)
        title = request.data.get("title", "New Consultation").strip() or "New Consultation"
        session = ChatSession.objects.create(patient=patient, title=title)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatSessionDetailView(APIView):
    """Retrieve or delete a specific chat session for current authenticated patient"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        patient = get_or_create_patient_for_user(request.user)
        session = get_object_or_404(ChatSession, id=pk, patient=patient)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_or_create_patient_for_user(request.user)
        session = get_object_or_404(ChatSession, id=pk, patient=patient)
        session.delete()
        return Response({"message": "Session deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class MedicationSearchAPIView(APIView):
    """Search verified medication knowledge base by name, brand, or indication"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q", "").strip()
        if not q:
            docs = MedicationDocument.objects.all()[:20]
        else:
            docs = MedicationDocument.objects.filter(
                Q(medication_name__icontains=q)
                | Q(generic_name__icontains=q)
                | Q(content__icontains=q)
            )[:30]

        serializer = MedicationDocumentSerializer(docs, many=True)
        return Response(serializer.data)


class MedicationDetailAPIView(APIView):
    """Get all sections and source documentation for a specific medication"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        doc = get_object_or_404(MedicationDocument, id=pk)
        all_sections = MedicationDocument.objects.filter(
            generic_name__iexact=doc.generic_name, source=doc.source
        )
        return Response({
            "medication_name": doc.medication_name,
            "generic_name": doc.generic_name,
            "brand_names": doc.brand_names,
            "active_ingredients": doc.active_ingredients,
            "source": doc.source,
            "source_url": doc.source_url,
            "document_id": doc.document_id,
            "sections": MedicationDocumentSerializer(all_sections, many=True).data,
        })


class SyncMedicationsAPIView(APIView):
    """Admin / Developer endpoint to trigger knowledge base sync"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        pipeline = MedicationIngestionPipeline()
        stats = pipeline.seed_all_verified_monographs()
        return Response({
            "message": "Medication knowledge base sync complete.",
            "stats": stats,
            "total_documents": MedicationDocument.objects.count(),
        })
