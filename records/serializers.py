from rest_framework import serializers
from .models import DailyRecord


class DailyRecordSerializer(serializers.ModelSerializer):
    pet_name = serializers.CharField(source="pet.name", read_only=True)
    supplements_list = serializers.SerializerMethodField()

    class Meta:
        model = DailyRecord
        fields = [
            "id",
            "pet",
            "pet_name",
            "recorded_at",
            "weight_kg",
            "water_ml",
            "food_g",
            "supplements_list",
            "mood",
            "poop_and_pee_count",
            "poop_status",
            "exercise_min",
            "medications",
            "note",
            "created_at",
            "updated_at",
        ]

    def get_supplements_list(self, obj):
        if not obj.supplements:
            return []
        return [s for s in obj.supplements.split(",") if s]
