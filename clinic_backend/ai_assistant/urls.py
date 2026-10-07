from django.urls import path
from ai_assistant.views import (
    PatientChatAPIView,
    ChatSessionListView,
    ChatSessionDetailView,
    MedicationSearchAPIView,
    MedicationDetailAPIView,
)

urlpatterns = [
    path("chat/", PatientChatAPIView.as_view(), name="ai_patient_chat"),
    path("sessions/", ChatSessionListView.as_view(), name="ai_chat_sessions"),
    path("sessions/<uuid:pk>/", ChatSessionDetailView.as_view(), name="ai_chat_session_detail"),
    path("medications/search/", MedicationSearchAPIView.as_view(), name="ai_medication_search"),
    path("medications/<int:pk>/", MedicationDetailAPIView.as_view(), name="ai_medication_detail"),
]
