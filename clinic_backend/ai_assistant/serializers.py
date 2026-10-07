from rest_framework import serializers
from ai_assistant.models import MedicationDocument, ChatSession, ChatMessage


class MedicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationDocument
        fields = [
            "id",
            "medication_name",
            "generic_name",
            "brand_names",
            "active_ingredients",
            "section",
            "section_title",
            "content",
            "source",
            "source_url",
            "document_id",
            "document_version",
            "last_updated",
            "created_at",
        ]


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "session",
            "role",
            "content",
            "intent",
            "symptoms",
            "medications_data",
            "sources",
            "red_flags",
            "doctor_review_required",
            "is_emergency",
            "created_at",
        ]


class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "patient",
            "title",
            "clinical_context",
            "created_at",
            "updated_at",
            "messages",
            "last_message",
        ]
        read_only_fields = ["patient", "created_at", "updated_at"]

    def get_last_message(self, obj):
        # Use prefetched in-memory messages if available to prevent N+1 remote database roundtrips
        if hasattr(obj, "_prefetched_objects_cache") and "messages" in obj._prefetched_objects_cache:
            msgs = obj._prefetched_objects_cache["messages"]
            if msgs:
                last_msg = sorted(msgs, key=lambda m: m.created_at, reverse=True)[0]
                return {
                    "role": last_msg.role,
                    "content": last_msg.content[:100] + ("..." if len(last_msg.content) > 100 else ""),
                    "created_at": last_msg.created_at,
                }
            return None
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return {
                "role": last_msg.role,
                "content": last_msg.content[:100] + ("..." if len(last_msg.content) > 100 else ""),
                "created_at": last_msg.created_at,
            }
class ChatSessionListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "patient",
            "title",
            "clinical_context",
            "created_at",
            "updated_at",
            "last_message",
        ]
        read_only_fields = ["patient", "created_at", "updated_at"]

    def get_last_message(self, obj):
        if hasattr(obj, "_prefetched_objects_cache") and "messages" in obj._prefetched_objects_cache:
            msgs = obj._prefetched_objects_cache["messages"]
            if msgs:
                last_msg = sorted(msgs, key=lambda m: m.created_at, reverse=True)[0]
                return {
                    "role": last_msg.role,
                    "content": last_msg.content[:100] + ("..." if len(last_msg.content) > 100 else ""),
                    "created_at": last_msg.created_at,
                }
            return None
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return {
                "role": last_msg.role,
                "content": last_msg.content[:100] + ("..." if len(last_msg.content) > 100 else ""),
                "created_at": last_msg.created_at,
            }
        return None
