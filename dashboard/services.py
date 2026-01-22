from __future__ import annotations
from typing import Any, List, Optional, Tuple, Dict
from django.apps import apps
from django.db.models import Sum, Value, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone


EVENT_MODEL_CANDIDATES = [
    ("planner", "Event"),
]

EXPENSE_MODEL_CANDIDATES = [
    ("expenses", "Expense"),
]


def _get_model(candidates: List[Tuple[str, str]]):
    for app_label, model_name in candidates:
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            continue
    return None


def _find_field(model, names: List[str]) -> Optional[str]:
    fields = {f.name for f in model._meta.get_fields()}
    for n in names:
        if n in fields:
            return n
    return None


def _filter_by_user(qs, model, user):
    user_field = _find_field(model, ["owner", "user", "created_by", "account"])
    if user_field:
        return qs.filter(**{user_field: user})
    return qs


def _filter_by_pet(qs, model, pet_id: Optional[int]):
    if not pet_id:
        return qs
    pet_field = _find_field(model, ["pet"])
    if pet_field:
        return qs.filter(**{f"{pet_field}_id": pet_id})
    return qs


def _decimal_coalesce_sum(model, field_name: str):
    f = model._meta.get_field(field_name)
    out = DecimalField(max_digits=getattr(f, "max_digits", 12), decimal_places=getattr(f, "decimal_places", 2))
    return Coalesce(Sum(field_name), Value(0, output_field=out), output_field=out)


def get_unread_reminders(user, pet_id: Optional[int] = None, limit: int = 20) -> List[Any]:
    Event = _get_model(EVENT_MODEL_CANDIDATES)
    if Event is None:
        return []

    remind_field = _find_field(Event, ["remind_at", "reminder_at", "notify_at"])
    if not remind_field:
        return []

    read_field = _find_field(Event, ["is_read", "read", "remind_read", "reminder_read"])
    now = timezone.now()

    qs = Event.objects.all()
    qs = _filter_by_user(qs, Event, user)
    qs = _filter_by_pet(qs, Event, pet_id)

    qs = qs.filter(**{f"{remind_field}__isnull": False, f"{remind_field}__lte": now})
    if read_field:
        qs = qs.filter(**{read_field: False})

    return list(qs.order_by(remind_field)[:limit])


def get_today_todos(user, pet_id: Optional[int] = None, limit: int = 20) -> List[Any]:
    Event = _get_model(EVENT_MODEL_CANDIDATES)
    if Event is None:
        return []

    start_field = _find_field(Event, ["start_at", "event_at", "scheduled_at"])
    if not start_field:
        return []

    status_field = _find_field(Event, ["status", "state"])
    done_values = {"done", "completed", "finish", "closed"}

    today = timezone.localdate()
    start_dt = timezone.make_aware(timezone.datetime(today.year, today.month, today.day, 0, 0, 0))
    end_dt = start_dt + timezone.timedelta(days=1)

    qs = Event.objects.all()
    qs = _filter_by_user(qs, Event, user)
    qs = _filter_by_pet(qs, Event, pet_id)

    qs = qs.filter(**{f"{start_field}__gte": start_dt, f"{start_field}__lt": end_dt})
    if status_field:
        qs = qs.exclude(**{f"{status_field}__in": list(done_values)})

    return list(qs.order_by(start_field)[:limit])


def get_month_total_expense(user, pet_id: Optional[int] = None, year: Optional[int] = None, month: Optional[int] = None) -> float:
    Expense = _get_model(EXPENSE_MODEL_CANDIDATES)
    if Expense is None:
        return 0.0

    date_field = _find_field(Expense, ["date", "spent_on", "created_at"])
    amount_field = _find_field(Expense, ["amount", "money", "cost", "price"])
    if not (date_field and amount_field):
        return 0.0

    today = timezone.localdate()
    year = year or today.year
    month = month or today.month

    qs = Expense.objects.all()
    qs = _filter_by_user(qs, Expense, user)
    qs = _filter_by_pet(qs, Expense, pet_id)

    qs = qs.filter(**{f"{date_field}__year": year, f"{date_field}__month": month})
    agg = qs.aggregate(total=_decimal_coalesce_sum(Expense, amount_field))
    return float(agg["total"] or 0)


def get_due_reminders(user, pet_id: Optional[int] = None, limit: int = 20) -> List[Any]:
    return get_unread_reminders(user, pet_id=pet_id, limit=limit)


def get_today_events(user, pet_id: Optional[int] = None, limit: int = 20) -> List[Any]:
    return get_today_todos(user, pet_id=pet_id, limit=limit)
