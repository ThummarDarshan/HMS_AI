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
from ai_assistant.safety.clarification_engine import ClinicalStateEngine
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
        if is_emergency:
            assistant_msg = ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=emergency_guidance,
                intent="EMERGENCY",
                red_flags=red_flags,
                doctor_review_required=True,
                is_emergency=True,
            )
            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "EMERGENCY",
                "answer": emergency_guidance,
                "symptoms": [],
                "medications": [],
                "sources": [],
                "redFlags": red_flags,
                "allergyConflicts": [],
                "doctorReviewRequired": True,
                "emergency": True,
                "informationComplete": False,
            })

        # 4. Check if it's a Pure Informational Monograph Query (e.g. 'What is paracetamol used for?')
        is_pure_info = ClinicalStateEngine.is_pure_monograph_query(message_text)
        is_prescription_req = PrescriptionGuard.is_prescription_request(message_text)

        # 5. Step 2: Clinical State & Clarification Questioning
        if not is_pure_info:
            clinical_state = ClinicalStateEngine.evaluate_clinical_state(
                current_message=message_text,
                chat_history=past_messages,
                patient=patient,
            )

            # If we do not have enough symptom context yet, ask dynamic clarification questions
            if not clinical_state.get("informationComplete", False):
                clarification_answer = ClinicalStateEngine.generate_clarification_response(
                    state=clinical_state,
                    user_message=message_text,
                )

                assistant_msg = ChatMessage.objects.create(
                    session=session,
                    role="assistant",
                    content=clarification_answer,
                    intent="SYMPTOM_CLARIFICATION",
                    symptoms=clinical_state.get("detectedProtocols", []),
                    doctor_review_required=True,
                    is_emergency=False,
                )
                session.save()

                return Response({
                    "success": True,
                    "session_id": str(session.id),
                    "intent": "SYMPTOM_CLARIFICATION",
                    "answer": clarification_answer,
                    "symptoms": clinical_state.get("detectedProtocols", []),
                    "medications": [],
                    "sources": [],
                    "redFlags": [],
                    "allergyConflicts": [],
                    "doctorReviewRequired": True,
                    "emergency": False,
                    "informationComplete": False,
                })

        # 6. Step 3: Grounded Document Retrieval
        retrieved = MedicationRetrievalEngine.retrieve(message_text)
        medications_data = retrieved.get("medications", [])
        sources = retrieved.get("sources", [])
        symptoms = retrieved.get("symptoms", [])
        intent = "PRESCRIPTION_REQUEST" if is_prescription_req else ("MEDICATION_INFORMATION" if is_pure_info else "SYMPTOM_ASSESSMENT")

        # 7. Step 4: Patient Profile Allergy Conflict Check
        med_names_to_check = [m["name"] for m in medications_data] + [m.get("generic_name", "") for m in medications_data]
        allergy_conflicts = AllergyChecker.check_patient_allergies(patient, med_names_to_check)

        # 8. Step 5: LLM / Grounded Synthesis
        patient_ctx = {
            "full_name": user.full_name if hasattr(user, "full_name") else user.username,
            "allergies": patient.allergies or "",
            "medical_history": patient.medical_history or "",
        }

        llm = get_llm_provider()
        answer = llm.generate_chat_response(
            user_message=message_text,
            retrieved_context=retrieved,
            patient_context=patient_ctx,
        )

        if is_prescription_req:
            disclaimer = PrescriptionGuard.get_anti_prescription_disclaimer()
            answer = f"{disclaimer}\n\n{answer}"

        # 9. Store Assistant Response in Session History
        assistant_msg = ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=answer,
            intent=intent,
            symptoms=symptoms,
            medications_data=medications_data,
            sources=sources,
            red_flags=[],
            doctor_review_required=True,
            is_emergency=False,
        )
        session.save()

        return Response({
            "success": True,
            "session_id": str(session.id),
            "intent": intent,
            "answer": answer,
            "symptoms": symptoms,
            "medications": medications_data,
            "sources": sources,
            "redFlags": [],
            "allergyConflicts": allergy_conflicts,
            "doctorReviewRequired": True,
            "emergency": False,
            "informationComplete": True,
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
