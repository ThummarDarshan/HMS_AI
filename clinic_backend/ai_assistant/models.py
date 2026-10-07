import uuid
from django.db import models
from patients.models import Patient


class MedicationDocument(models.Model):
    SOURCE_CHOICES = [
        ("CDSCO", "CDSCO (Govt of India)"),
        ("DAILYMED", "DailyMed (FDA SPL)"),
        ("OPENFDA", "OpenFDA Drug Label"),
        ("MANUFACTURER", "Manufacturer Monograph"),
    ]

    SECTION_CHOICES = [
        ("INDICATIONS", "Indications and Usage"),
        ("WARNINGS", "Warnings and Precautions"),
        ("CONTRAINDICATIONS", "Contraindications"),
        ("ADVERSE_REACTIONS", "Adverse Reactions / Side Effects"),
        ("DRUG_INTERACTIONS", "Drug Interactions"),
        ("DOSAGE_AND_ADMINISTRATION", "Dosage and Administration"),
        ("PATIENT_INFORMATION", "Patient Counseling Information"),
        ("GENERAL_SUMMARY", "General Summary & Composition"),
    ]

    medication_name = models.CharField(max_length=255, db_index=True)
    generic_name = models.CharField(max_length=255, db_index=True)
    brand_names = models.JSONField(default=list, blank=True)
    active_ingredients = models.JSONField(default=list, blank=True)
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, db_index=True)
    section_title = models.CharField(max_length=255)
    content = models.TextField()
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="CDSCO", db_index=True)
    source_url = models.URLField(max_length=500)
    document_id = models.CharField(max_length=100, blank=True, null=True)
    document_version = models.CharField(max_length=50, blank=True, null=True)
    last_updated = models.CharField(max_length=100, blank=True, null=True)
    embedding = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_medication_documents"
        verbose_name = "Medication Document"
        verbose_name_plural = "Medication Documents"
        indexes = [
            models.Index(fields=["generic_name", "section"]),
            models.Index(fields=["source", "medication_name"]),
        ]

    def __str__(self):
        return f"{self.medication_name} - {self.section} ({self.source})"


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="ai_chat_sessions"
    )
    title = models.CharField(max_length=255, default="Health Consultation")
    clinical_context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_chat_sessions"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Chat Session ({self.patient.user.full_name}) - {self.title}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    intent = models.CharField(max_length=50, blank=True, null=True)
    symptoms = models.JSONField(default=list, blank=True)
    medications_data = models.JSONField(default=list, blank=True)
    sources = models.JSONField(default=list, blank=True)
    red_flags = models.JSONField(default=list, blank=True)
    doctor_review_required = models.BooleanField(default=True)
    is_emergency = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_chat_messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role.upper()}] {self.session.id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
