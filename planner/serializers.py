from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source="pet.name", read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "pet",
            "pet_name",
            "title",
            "type",
            "status",
            "start_at",
            "end_at",
            "all_day",
            "description",
            "remind_at",
            "reminded_at",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "reminded_at"]
