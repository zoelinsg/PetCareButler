from datetime import date as _date, datetime as _datetime, time as _time
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import DailyRecordForm
from .models import DailyRecord
from pets.models import Pets


def _to_datetime_local_string(value) -> str:
    if isinstance(value, _datetime):
        dt = value
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        dt = timezone.localtime(dt)
        return dt.strftime("%Y-%m-%dT%H:%M")

    if isinstance(value, _date):
        dt = _datetime.combine(value, _time(0, 0))
        return dt.strftime("%Y-%m-%dT%H:%M")

    return timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M")


class OwnerPetQuerysetMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if "pet" in form.fields:
            form.fields["pet"].queryset = Pets.objects.filter(
                owner=self.request.user, is_deceased=False
            ).order_by("name")

        if "recorded_at" in form.fields and not form.initial.get("recorded_at"):
            form.initial["recorded_at"] = timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M")

        return form


class DailyRecordOwnerOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.pet.owner == self.request.user


class DailyRecordListView(LoginRequiredMixin, ListView):
    model = DailyRecord
    template_name = "care/record_list.html"
    context_object_name = "records"
    paginate_by = 20

    def get_queryset(self):
        qs = DailyRecord.objects.filter(
            pet__owner=self.request.user,
            pet__is_deceased=False,
        )

        pet_id = self.kwargs.get("pet_id") or (self.request.GET.get("pet") or "").strip()
        q = (self.request.GET.get("q") or "").strip()

        if str(pet_id).isdigit():
            qs = qs.filter(pet_id=int(pet_id))

        if q:
            qs = qs.filter(
                Q(note__icontains=q)
                | Q(supplements__icontains=q)
                | Q(medications__icontains=q)
            )

        return qs.select_related("pet")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()

        pet_id = self.kwargs.get("pet_id") or (self.request.GET.get("pet") or "").strip()
        ctx["pet"] = str(pet_id) if pet_id else ""

        ctx["pets"] = Pets.objects.filter(
            owner=self.request.user, is_deceased=False
        ).order_by("name")

        return ctx


class DailyRecordDetailView(LoginRequiredMixin, DailyRecordOwnerOnlyMixin, DetailView):
    model = DailyRecord
    template_name = "care/record_detail.html"
    context_object_name = "record"


class DailyRecordCreateView(LoginRequiredMixin, OwnerPetQuerysetMixin, CreateView):
    model = DailyRecord
    form_class = DailyRecordForm
    template_name = "care/record_form.html"
    success_url = reverse_lazy("care_record_list")

    def get_initial(self):
        initial = super().get_initial()

        pet_id = self.kwargs.get("pet_id") or self.request.GET.get("pet")
        if pet_id and str(pet_id).isdigit():
            initial["pet"] = int(pet_id)

        initial.setdefault("recorded_at", timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M"))
        return initial


class DailyRecordUpdateView(LoginRequiredMixin, DailyRecordOwnerOnlyMixin, OwnerPetQuerysetMixin, UpdateView):
    model = DailyRecord
    form_class = DailyRecordForm
    template_name = "care/record_form.html"

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial["recorded_at"] = _to_datetime_local_string(obj.recorded_at)
        return initial

    def get_success_url(self):
        return reverse_lazy("care_record_detail", kwargs={"pk": self.object.pk})


class DailyRecordDeleteView(LoginRequiredMixin, DailyRecordOwnerOnlyMixin, DeleteView):
    model = DailyRecord
    template_name = "care/record_delete.html"
    success_url = reverse_lazy("care_record_list")
