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

    def test_fever_one_by_one_flow(self):
        """Test strict one-question-at-a-time conversation for fever"""
        self.client.force_authenticate(user=self.user_b)  # No DOB in profile

        # Turn 1: User reports fever -> Assistant asks age
        turn1 = self.client.post("/api/ai-assistant/chat/", {"message": "I have fever"}, format="json")
        self.assertEqual(turn1.status_code, status.HTTP_200_OK)
        d1 = turn1.json()
        session_id = d1["session_id"]
        self.assertEqual(d1["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(d1["informationComplete"])
        self.assertEqual(len(d1["medications"]), 0)  # No monograph dump!
        self.assertIn("how old are you", d1["answer"].lower())
        self.assertNotIn("how many days", d1["answer"].lower())

        # Turn 2: User answers age 20 -> Assistant asks duration
        turn2 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "20"}, format="json")
        d2 = turn2.json()
        self.assertEqual(d2["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(d2["informationComplete"])
        self.assertIn("how long have you had the fever", d2["answer"].lower())

        # Turn 3: User answers 2 days -> Assistant asks temperature
        turn3 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "2 days"}, format="json")
        d3 = turn3.json()
        self.assertEqual(d3["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(d3["informationComplete"])
        self.assertIn("temperature", d3["answer"].lower())

        # Turn 4: User answers 102°F -> Assistant asks other symptoms
        turn4 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "102°F"}, format="json")
        d4 = turn4.json()
        self.assertEqual(d4["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(d4["informationComplete"])
        self.assertIn("other symptoms", d4["answer"].lower())

        # Turn 5: User answers other symptoms -> Full structured assessment
        turn5 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "just mild headache and body aches"}, format="json")
        d5 = turn5.json()
        self.assertEqual(d5["intent"], "AI_CONSULTATION")
        self.assertTrue(d5["informationComplete"])
        self.assertIn("### Summary", d5["answer"])
        self.assertIn("### What your symptoms may indicate", d5["answer"])
        self.assertIn("### Warning signs", d5["answer"])
        self.assertIn("### General self-care", d5["answer"])
        self.assertIn("### Medication information", d5["answer"])
        self.assertIn("### When to see a doctor", d5["answer"])
        self.assertIn("### Sources", d5["answer"])

    def test_fever_context_memory_skip_redundant_questions(self):
        """Test that already provided info (age and duration) is NOT asked again"""
        self.client.force_authenticate(user=self.user_b)
        res = self.client.post("/api/ai-assistant/chat/", {
            "message": "I'm 20 years old and have had fever for 2 days"
        }, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(data["informationComplete"])
        # Should NOT ask age or duration again!
        self.assertNotIn("how old are you", data["answer"].lower())
        self.assertNotIn("how long have you had", data["answer"].lower())
        # Should ask temperature
        self.assertIn("temperature", data["answer"].lower())

    def test_chest_pain_early_red_flag_screening(self):
        """Test chest pain triggers early red-flag screening question"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have chest pain"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertFalse(data["informationComplete"])
        self.assertIn("screening", data["answer"].lower())
        self.assertIn("severe or crushing", data["answer"].lower())

    def test_emergency_severe_chest_pain_and_breathing(self):
        """Test acute emergency scenario triggers immediate stop and emergency helpline guidance"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have severe chest pain and difficulty breathing"
        }, format="json")
        data = res.json()
        self.assertTrue(data["emergency"])
        self.assertEqual(data["intent"], "EMERGENCY")
        self.assertIn("108", data["answer"])

    def test_shortness_of_breath_emergency_screening(self):
        """Test shortness of breath triggers emergency screening question"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I'm having difficulty breathing"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("breathing difficulty requires immediate safety assessment", data["answer"].lower())

    def test_cough_one_by_one_flow(self):
        """Test cough conversation flow"""
        self.client.force_authenticate(user=self.user_a)  # Age known
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have a cough"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("cough", data["answer"].lower())

    def test_abdominal_pain_flow(self):
        """Test stomach ache conversation flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "My stomach hurts"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("stomach", data["answer"].lower())

    def test_vomiting_flow(self):
        """Test vomiting inquiry flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have been vomiting"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("vomit", data["answer"].lower())

    def test_diarrhea_flow(self):
        """Test diarrhea inquiry flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have diarrhea"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("loose", data["answer"].lower())

    def test_sore_throat_flow(self):
        """Test sore throat flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "My throat hurts"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("throat", data["answer"].lower())

    def test_dizziness_flow(self):
        """Test dizziness inquiry flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I feel dizzy"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("dizz", data["answer"].lower())

    def test_back_pain_flow(self):
        """Test back pain inquiry flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have back pain"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("back", data["answer"].lower())

    def test_skin_rash_flow(self):
        """Test skin rash inquiry flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have a rash"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("rash", data["answer"].lower())

    def test_diabetes_question_flow(self):
        """Test chronic diabetes question flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have diabetes"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("diabetes", data["answer"].lower())

    def test_hypertension_question_flow(self):
        """Test hypertension question flow"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {"message": "I have high blood pressure"}, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("blood pressure", data["answer"].lower())

    def test_multiple_symptoms_cluster(self):
        """Test cluster of multiple symptoms handled cohesively"""
        self.client.force_authenticate(user=self.user_a)
        res = self.client.post("/api/ai-assistant/chat/", {
            "message": "I have fever, cough and headache"
        }, format="json")
        data = res.json()
        self.assertEqual(data["intent"], "SYMPTOM_CLARIFICATION")
        self.assertIn("fever", data["answer"].lower())

    def test_followup_question_after_assessment(self):
        """Test follow-up question in completed consultation does not restart questionnaire"""
        self.client.force_authenticate(user=self.user_a)
        # Turn 1
        turn1 = self.client.post("/api/ai-assistant/chat/", {"message": "I have a headache since yesterday"}, format="json")
        session_id = turn1.json()["session_id"]
        # Turn 2 - Complete assessment
        turn2 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "It is a mild headache, no vision changes or fever"}, format="json")
        self.assertTrue(turn2.json()["informationComplete"])

        # Turn 3 - Follow-up: home care
        turn3 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "What can I do at home?"}, format="json")
        d3 = turn3.json()
        self.assertEqual(d3["intent"], "FOLLOW_UP_GUIDANCE")
        self.assertTrue(d3["informationComplete"])
        self.assertIn("home self-care", d3["answer"].lower())

        # Turn 4 - Follow-up: medication safety
        turn4 = self.client.post("/api/ai-assistant/chat/", {"session_id": session_id, "message": "Is paracetamol safe?"}, format="json")
        d4 = turn4.json()
        self.assertEqual(d4["intent"], "FOLLOW_UP_GUIDANCE")
        self.assertTrue(d4["informationComplete"])
        self.assertIn("paracetamol", d4["answer"].lower())

