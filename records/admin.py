from django.contrib import admin
from .models import DailyRecord


@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id", "pet", "recorded_at",
        "weight_kg", "water_ml", "food_g",
        "poop_and_pee_count", "poop_status",
        "mood",
    )
    list_filter = ("mood", "poop_status", "recorded_at")
    search_fields = ("pet__name", "supplements", "medications", "note")
    date_hierarchy = "recorded_at"
