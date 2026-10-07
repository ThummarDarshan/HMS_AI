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
    ChatSessionListSerializer,
    ChatMessageSerializer,
)
from ai_assistant.safety.emergency_detector import EmergencyDetector
from ai_assistant.safety.allergy_checker import AllergyChecker
from ai_assistant.safety.prescription_guard import PrescriptionGuard
from ai_assistant.safety.clarification_engine import ClinicalStateEngine
from ai_assistant.clinical.conversation_engine import UniversalClinicalEngine
from ai_assistant.retrieval.search import MedicationRetrievalEngine
from ai_assistant.llm.provider import get_llm_provider

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
    Core AI Health Assistant Chat API.
    Operates directly via Google Gemini API key.
    Provides intelligent medical guidance, symptom assistance, first aid advice,
    and emergency red-flag screening.
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

        past_messages = list(session.messages.order_by("created_at"))

        # 2. Record User Message
        user_msg = ChatMessage.objects.create(
            session=session,
            role="user",
            content=message_text,
        )

        # 3. Emergency Red Flag Screening (HIGHEST PRIORITY)
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
            session.save()
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
                "informationComplete": True,
            })

        # 4. Anti-prescription detection & Prompt Injection Check
        is_injection = PrescriptionGuard.detect_prompt_injection(message_text)
        if is_injection:
            safety_msg = (
                "I am Velora AI Care, a safety-focused clinical assistant. "
                "I cannot bypass safety guidelines or alter my role as an educational medical assistant. "
                "How can I assist you with your health or hospital services today?"
            )
            ChatMessage.objects.create(session=session, role="assistant", content=safety_msg, intent="SAFETY_POLICY")
            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "SAFETY_POLICY",
                "answer": safety_msg,
                "symptoms": [],
                "medications": [],
                "sources": [],
                "redFlags": [],
                "allergyConflicts": [],
                "doctorReviewRequired": False,
                "emergency": False,
                "informationComplete": True,
            })

        is_prescription_req = PrescriptionGuard.is_prescription_request(message_text)

        # 5. Pure Informational / Monograph vs Stateful Clinical Consultation
        is_pure_monograph = ClinicalStateEngine.is_pure_monograph_query(message_text)

        if is_pure_monograph:
            retrieval_res = MedicationRetrievalEngine.retrieve(message_text)
            sources = retrieval_res.get("sources", [])
            medications_data = retrieval_res.get("medications", [])
            target_drugs = retrieval_res.get("target_drugs", [])

            allergy_conflicts = []
            if target_drugs:
                allergy_conflicts = AllergyChecker.check_patient_allergies(patient, target_drugs)

            patient_age = getattr(patient, "age", None)
            if not patient_age and hasattr(patient, "date_of_birth") and patient.date_of_birth:
                import datetime
                today = datetime.date.today()
                dob = patient.date_of_birth
                patient_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            patient_ctx = {
                "full_name": user.full_name if hasattr(user, "full_name") else user.username,
                "allergies": patient.allergies or "",
                "medical_history": patient.medical_history or "",
                "gender": getattr(patient, "gender", ""),
                "age": patient_age or "",
            }

            llm = get_llm_provider()
            answer = llm.generate_chat_response(
                user_message=message_text,
                chat_history=past_messages,
                patient_context=patient_ctx,
            )

            intent = "MEDICATION_INFORMATION" if (target_drugs or medications_data) else "AI_CONSULTATION"
            if is_prescription_req:
                disclaimer = PrescriptionGuard.get_anti_prescription_disclaimer()
                if "Medication Safety Notice" not in answer:
                    answer = f"{disclaimer}\n\n{answer}"
                intent = "PRESCRIPTION_REQUEST"

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=answer,
                intent=intent,
                symptoms=retrieval_res.get("symptoms", []),
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
                "symptoms": retrieval_res.get("symptoms", []),
                "medications": medications_data,
                "sources": sources,
                "redFlags": [],
                "allergyConflicts": allergy_conflicts,
                "doctorReviewRequired": True,
                "emergency": False,
                "informationComplete": True,
            })

        # 6. Universal Clinical Conversation Engine (Stateful, One Question at a Time)
        turn_result = UniversalClinicalEngine.evaluate_turn(
            user_message=message_text,
            session_context=session.clinical_context,
            patient=patient,
            chat_history=past_messages,
        )

        # Handle emergency triggered during conversation turn
        if turn_result.get("is_emergency"):
            emergency_ans = turn_result["answer"]
            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=emergency_ans,
                intent="EMERGENCY",
                red_flags=turn_result.get("red_flags", []),
                doctor_review_required=True,
                is_emergency=True,
            )
            session.clinical_context = turn_result.get("context", {})
            session.save()
            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "EMERGENCY",
                "answer": emergency_ans,
                "symptoms": turn_result.get("symptoms", []),
                "medications": [],
                "sources": [],
                "redFlags": turn_result.get("red_flags", []),
                "allergyConflicts": [],
                "doctorReviewRequired": True,
                "emergency": True,
                "informationComplete": True,
            })

        # If general health question (e.g. general curiosity not matching clinical conditions)
        if turn_result.get("intent") == "GENERAL_HEALTH":
            retrieval_res = MedicationRetrievalEngine.retrieve(message_text)
            patient_age = getattr(patient, "age", None)
            if not patient_age and hasattr(patient, "date_of_birth") and patient.date_of_birth:
                import datetime
                today = datetime.date.today()
                dob = patient.date_of_birth
                patient_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            patient_ctx = {
                "full_name": user.full_name if hasattr(user, "full_name") else user.username,
                "allergies": patient.allergies or "",
                "medical_history": patient.medical_history or "",
                "gender": getattr(patient, "gender", ""),
                "age": patient_age or "",
            }

            llm = get_llm_provider()
            answer = llm.generate_chat_response(
                user_message=message_text,
                chat_history=past_messages,
                patient_context=patient_ctx,
            )
            if is_prescription_req:
                disclaimer = PrescriptionGuard.get_anti_prescription_disclaimer()
                if "Medication Safety Notice" not in answer:
                    answer = f"{disclaimer}\n\n{answer}"

            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=answer,
                intent="AI_CONSULTATION",
                symptoms=[],
                medications_data=[],
                sources=retrieval_res.get("sources", []),
                red_flags=[],
                doctor_review_required=True,
                is_emergency=False,
            )
            session.save()

            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "AI_CONSULTATION",
                "answer": answer,
                "symptoms": [],
                "medications": [],
                "sources": retrieval_res.get("sources", []),
                "redFlags": [],
                "allergyConflicts": [],
                "doctorReviewRequired": True,
                "emergency": False,
                "informationComplete": True,
            })

        # If Asking ONE QUESTION AT A TIME
        if turn_result.get("intent") == "SYMPTOM_CLARIFICATION":
            session.clinical_context = turn_result.get("context", {})
            # Update session title if first turn
            if session.messages.filter(role="assistant").count() == 0 and turn_result.get("symptoms"):
                session.title = f"Consultation: {turn_result['symptoms'][0]}"
            session.save()

            clarification_answer = turn_result["answer"]
            ChatMessage.objects.create(
                session=session,
                role="assistant",
                content=clarification_answer,
                intent="SYMPTOM_CLARIFICATION",
                symptoms=turn_result.get("symptoms", []),
                medications_data=[],  # Crucial: never dump monograph during questioning!
                sources=[],           # Crucial: never dump sources during questioning!
                red_flags=[],
                doctor_review_required=True,
                is_emergency=False,
            )

            return Response({
                "success": True,
                "session_id": str(session.id),
                "intent": "SYMPTOM_CLARIFICATION",
                "answer": clarification_answer,
                "symptoms": turn_result.get("symptoms", []),
                "medications": [],
                "sources": [],
                "redFlags": [],
                "allergyConflicts": [],
                "doctorReviewRequired": True,
                "emergency": False,
                "informationComplete": False,
            })

        # If Clinical Consultation Summary Complete or Follow-up Guidance
        session.clinical_context = turn_result.get("context", {})
        session.save()

        # Retrieve verified medication documentation for condition
        query_for_retrieval = " ".join(turn_result.get("symptoms", []) + [message_text])
        retrieval_res = MedicationRetrievalEngine.retrieve(query_for_retrieval)
        target_drugs = retrieval_res.get("target_drugs", [])
        allergy_conflicts = AllergyChecker.check_patient_allergies(patient, target_drugs) if target_drugs else []

        meds = retrieval_res.get("medications", []) or turn_result.get("medications", [])
        srcs = retrieval_res.get("sources", []) or turn_result.get("sources", [])

        final_answer = turn_result["answer"]
        if is_prescription_req:
            disclaimer = PrescriptionGuard.get_anti_prescription_disclaimer()
            if "Medication Safety Notice" not in final_answer:
                final_answer = f"{disclaimer}\n\n{final_answer}"

        intent = turn_result.get("intent", "AI_CONSULTATION")
        ChatMessage.objects.create(
            session=session,
            role="assistant",
            content=final_answer,
            intent=intent,
            symptoms=turn_result.get("symptoms", []),
            medications_data=meds,
            sources=srcs,
            red_flags=[],
            doctor_review_required=True,
            is_emergency=False,
        )

        return Response({
            "success": True,
            "session_id": str(session.id),
            "intent": intent,
            "answer": final_answer,
            "symptoms": turn_result.get("symptoms", []),
            "medications": meds,
            "sources": srcs,
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
        sessions = (
            ChatSession.objects
            .filter(patient=patient)
            .prefetch_related("messages")
            .order_by("-updated_at")
        )
        serializer = ChatSessionListSerializer(sessions, many=True)
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
        session = get_object_or_404(
            ChatSession.objects.prefetch_related("messages"),
            id=pk,
            patient=patient,
        )
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)

    def delete(self, request, pk):
        patient = get_or_create_patient_for_user(request.user)
        session = get_object_or_404(ChatSession, id=pk, patient=patient)
        session.delete()
        return Response({"message": "Session deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class MedicationSearchAPIView(APIView):
    """Search medication knowledge base by name, brand, or indication"""
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
