from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "pet",
        "title",
        "type",
        "status",
        "start_at",
        "end_at",
        "all_day",
        "remind_at",
        "reminded_at",
        "created_at",
        "updated_at",
    )
    list_filter = ("type", "status", "all_day", "start_at")
    search_fields = ("pet__name", "title", "description", "note")
    date_hierarchy = "start_at"
    list_select_related = ("pet", "created_by")
