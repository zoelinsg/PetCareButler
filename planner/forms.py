from datetime import datetime, time
from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "pet",
            "title",
            "type",
            "start_at",
            "end_at",
            "all_day",
            "status",
            "description",
            "remind_at",
            "note",
        ]
        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "remind_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 3}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned = super().clean()
        start_at = cleaned.get("start_at")
        end_at = cleaned.get("end_at")
        all_day = cleaned.get("all_day")

        if end_at and start_at and end_at < start_at:
            self.add_error("end_at", "結束時間不能早於開始時間。")

        if all_day and start_at:
            tz = timezone.get_current_timezone()
            local_day = timezone.localtime(start_at, tz).date()
            cleaned["start_at"] = timezone.make_aware(datetime.combine(local_day, time.min), tz)
            cleaned["end_at"] = timezone.make_aware(datetime.combine(local_day, time.max), tz)

        return cleaned
