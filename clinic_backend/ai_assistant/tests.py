from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
import datetime
from patients.models import Patient
from ai_assistant.models import MedicationDocument, ChatSession, ChatMessage
from ai_assistant.safety.emergency_detector import EmergencyDetector
from ai_assistant.safety.allergy_checker import AllergyChecker
from ai_assistant.safety.prescription_guard import PrescriptionGuard
from ai_assistant.safety.clarification_engine import ClinicalStateEngine
from ai_assistant.retrieval.search import MedicationRetrievalEngine
from ai_assistant.providers.cdsco_provider import CDSCOProvider

User = get_user_model()


class AIAssistantSafetyAndRetrievalTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cdsco = CDSCOProvider()
        test_drugs = ["paracetamol", "ibuprofen", "amoxicillin"]
        docs = []
        for drug in test_drugs:
            chunks = cdsco.get_medication_details(drug)
            for c in chunks:
                docs.append(
                    MedicationDocument(
                        medication_name=c.medication_name,
                        generic_name=c.generic_name,
                        brand_names=c.brand_names,
                        active_ingredients=c.active_ingredients,
                        section=c.section,
                        section_title=c.section_title,
                        content=c.content,
                        source=c.source,
                        source_url=c.source_url,
                        document_id=c.document_id,
                        document_version=c.document_version,
                        last_updated=c.last_updated,
                    )
                )
        MedicationDocument.objects.bulk_create(docs)

        # Create Patient A with DOB (Age known) and Allergy
        cls.user_a = User.objects.create_user(
            email="patient.a@example.com",
            password="StrongPassword123!",
            role="PATIENT",
            first_name="Harshal",
            last_name="Shah",
        )
        cls.patient_a, _ = Patient.objects.get_or_create(user=cls.user_a)
        cls.patient_a.date_of_birth = datetime.date(2000, 5, 15)  # ~26 years old
        cls.patient_a.allergies = "Penicillin, Amoxicillin"
        cls.patient_a.medical_history = "Mild asthma"
        cls.patient_a.save()

        # Create Patient B without DOB
        cls.user_b = User.objects.create_user(
            email="patient.b@example.com",
            password="StrongPassword123!",
            role="PATIENT",
            first_name="Aryan",
            last_name="Patel",
        )
        cls.patient_b, _ = Patient.objects.get_or_create(user=cls.user_b)
        cls.patient_b.allergies = "None"
        cls.patient_b.save()

    def setUp(self):
        self.client = APIClient()

    def test_emergency_detector_chest_pain(self):
        """Test emergency red flag detection for acute cardiac symptoms"""
        is_emergency, flags, guidance = EmergencyDetector.evaluate("I have severe crushing chest pain radiating to left arm")
        self.assertTrue(is_emergency)
        self.assertTrue(len(flags) > 0)
        self.assertIn("108", guidance)

    def test_emergency_detector_breathing_difficulty(self):
        """Test emergency red flag detection for acute respiratory distress"""
        is_emergency, flags, guidance = EmergencyDetector.evaluate("I cannot breathe and my lips are turning blue")
        self.assertTrue(is_emergency)
        self.assertEqual(flags[0]["category"], "Acute Respiratory Distress")

    def test_prescription_guard_intent(self):
        """Test detection of prescription requests"""
        self.assertTrue(PrescriptionGuard.is_prescription_request("What medicine should I take for my fever?"))
        self.assertTrue(PrescriptionGuard.is_prescription_request("Please prescribe me an antibiotic"))
        self.assertFalse(PrescriptionGuard.is_prescription_request("What are the side effects of paracetamol?"))

    def test_allergy_conflict_detection(self):
        """Test that penicillin allergy is flagged when Amoxicillin is considered"""
        conflicts = AllergyChecker.check_patient_allergies(self.patient_a, ["Amoxicillin", "Paracetamol"])
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["severity"], "CRITICAL")
        self.assertIn("Amoxicillin", conflicts[0]["warning"])

    def test_grounded_medication_retrieval(self):
        """Test retrieval of verified CDSCO documentation for paracetamol"""
        retrieved = MedicationRetrievalEngine.retrieve("What are the warnings for paracetamol?")
        self.assertTrue(retrieved["has_verified_evidence"])
        self.assertTrue(len(retrieved["sources"]) > 0)
        self.assertTrue(any(s["source_type"] == "CDSCO" for s in retrieved["sources"]))

    def test_pure_monograph_query_direct_response(self):
        """Test pure informational query gets verified monograph directly without symptom questioning"""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post("/api/ai-assistant/chat/", {
            "message": "What is paracetamol used for?"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["intent"], "MEDICATION_INFORMATION")
        self.assertTrue(data["informationComplete"])
        self.assertTrue(len(data["sources"]) > 0)

    def test_symptom_triggers_conversational_clarification(self):
        """Test that initial symptom query triggers non-overwhelming clarification questions"""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have loose motion and stomach upset"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(data["informationComplete"])
        self.assertIn("loose motion", data["answer"].lower())
        # Since patient A has DOB in profile, "How old are you?" should NOT be asked
        self.assertNotIn("how old are you", data["answer"].lower())

    def test_age_asked_if_not_in_profile(self):
        """Test that age IS asked if patient profile has no DOB"""
        self.client.force_authenticate(user=self.user_b)
        response = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have loose motion"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("how old are you", data["answer"].lower())

    def test_multi_turn_clarification_flow(self):
        """Test complete multi-turn clarification from symptom to verified response"""
        self.client.force_authenticate(user=self.user_a)

        # Turn 1: Symptom
        turn1 = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have a headache since yesterday"
        }, format="json")
        session_id = turn1.json()["session_id"]
        self.assertEqual(turn1.json()["intent"], "SYMPTOM_CLARIFICATION")

        # Turn 2: Clarification response
        turn2 = self.client.post("/api/ai-assistant/chat/", {
            "session_id": session_id,
            "message": "It is a mild headache, no vision changes or fever"
        }, format="json")
        data2 = turn2.json()
        self.assertTrue(data2["informationComplete"])
        self.assertTrue(data2["doctorReviewRequired"])

    def test_emergency_chat_api_response(self):
        """Test emergency query halts normal recommendations and returns emergency guidance"""
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have crushing chest pain and feel like fainting"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertTrue(data["emergency"])
        self.assertEqual(data["intent"], "EMERGENCY")
        self.assertTrue(len(data["redFlags"]) > 0)

    def test_patient_session_ownership_isolation(self):
        """Ensure Patient B cannot access or delete Patient A's chat session"""
        session_a = ChatSession.objects.create(patient=self.patient_a, title="Patient A Consultation")

        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(f"/api/ai-assistant/sessions/{session_a.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        delete_response = self.client.delete(f"/api/ai-assistant/sessions/{session_a.id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_404_NOT_FOUND)
