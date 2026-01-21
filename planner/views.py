import calendar
from datetime import datetime, date, time, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventForm
from .models import Event


def _month_range(year: int, month: int):
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    start_dt = timezone.make_aware(datetime.combine(first_day, time.min))
    end_dt = timezone.make_aware(datetime.combine(last_day, time.max))
    return first_day, last_day, start_dt, end_dt


@login_required
def month_view(request):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    first_day, last_day, start_dt, end_dt = _month_range(year, month)

    qs = Event.objects.filter(
        start_at__range=(start_dt, end_dt),
        created_by=request.user,
    )

    events = list(qs.select_related("pet").order_by("start_at"))

    by_day = {}
    for e in events:
        by_day.setdefault(e.day, []).append(e)

    cal = calendar.Calendar(firstweekday=0)
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        weeks.append(
            [{"date": d, "in_month": (d.month == month), "events": by_day.get(d, [])} for d in week]
        )

    prev_month = (first_day - timedelta(days=1)).replace(day=1)
    next_month = (last_day + timedelta(days=1)).replace(day=1)

    context = {
        "year": year,
        "month": month,
        "weeks": weeks,
        "prev_year": prev_month.year,
        "prev_month": prev_month.month,
        "next_year": next_month.year,
        "next_month": next_month.month,
        "today": today,
    }
    return render(request, "planner/month.html", context)


@login_required
def day_view(request, year: int, month: int, day: int):
    d = date(year, month, day)
    start_dt = timezone.make_aware(datetime.combine(d, time.min))
    end_dt = timezone.make_aware(datetime.combine(d, time.max))

    qs = Event.objects.filter(
        start_at__range=(start_dt, end_dt),
        created_by=request.user,
    )

    context = {
        "day": d,
        "events": qs.select_related("pet").order_by("start_at"),
    }
    return render(request, "planner/day.html", context)


@login_required
def event_detail(request, pk: int):
    obj = get_object_or_404(Event.objects.select_related("pet"), pk=pk, created_by=request.user)
    return render(request, "planner/detail.html", {"event": obj})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect("detail", pk=obj.pk)
    else:
        form = EventForm()

    return render(request, "planner/form.html", {"mode": "create", "form": form})


@login_required
def event_update(request, pk: int):
    obj = get_object_or_404(Event, pk=pk, created_by=request.user)

    if request.method == "POST":
        form = EventForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("detail", pk=obj.pk)
    else:
        form = EventForm(instance=obj)

    return render(request, "planner/form.html", {"mode": "update", "form": form, "event": obj})


@login_required
def event_delete(request, pk: int):
    obj = get_object_or_404(Event, pk=pk, created_by=request.user)

    if request.method == "POST":
        obj.delete()
        return redirect("month")

    return render(request, "planner/delete.html", {"event": obj})


@login_required
def reminder_list(request):
    now = timezone.now()
    events = Event.objects.filter(
        remind_at__isnull=False,
        remind_at__lte=now,
        status=Event.Status.PLANNED,
        reminded_at__isnull=True,
        created_by=request.user,
    ).select_related("pet").order_by("remind_at", "start_at")

    return render(request, "planner/reminders.html", {"events": events})


@login_required
def reminder_mark_all(request):
    if request.method == "POST":
        now = timezone.now()
        Event.objects.filter(
            remind_at__isnull=False,
            remind_at__lte=now,
            status=Event.Status.PLANNED,
            reminded_at__isnull=True,
            created_by=request.user,
        ).update(reminded_at=now)

    return redirect("planner_reminders")
