from django.utils import timezone
from .models import Event

def reminder_context(request):
    if not request.user.is_authenticated:
        return {"reminder_count": 0}

    now = timezone.now()
    qs = Event.objects.filter(
        remind_at__isnull=False,
        remind_at__lte=now,
        status=Event.Status.PLANNED,
        reminded_at__isnull=True,
        created_by=request.user,
    )

    return {"reminder_count": qs.count()}
