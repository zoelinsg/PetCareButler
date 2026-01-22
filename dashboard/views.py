from __future__ import annotations
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import services


@login_required
def home(request):
    pet_id = request.GET.get("pet")
    try:
        pet_id = int(pet_id) if pet_id else None
    except ValueError:
        pet_id = None

    reminders = services.get_unread_reminders(request.user, pet_id=pet_id, limit=20)
    today_events = services.get_today_todos(request.user, pet_id=pet_id, limit=20)
    month_total = services.get_month_total_expense(request.user, pet_id=pet_id)

    context = {
        "pet_id": pet_id,
        "reminders": reminders,
        "reminders_count": len(reminders),
        "today_events": today_events,
        "today_events_count": len(today_events),
        "month_total_expense": month_total,
    }
    return render(request, "dashboard/dashboard.html", context)
