from urllib.parse import urlencode
from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_date
from .forms import ExpenseForm
from .models import Expense


def _user_field_name(model_cls):
    for name in ("user", "owner", "author"):
        if any(f.name == name for f in model_cls._meta.fields):
            return name
    return None


def _pet_field_exists(model_cls):
    return any(f.name == "pet" for f in model_cls._meta.fields)


def _safe_text_fields(model_cls, candidates):
    names = {f.name for f in model_cls._meta.fields}
    return [c for c in candidates if c in names]


def _get_user_pets(user):
    try:
        if hasattr(user, "pets"):
            return user.pets.all()
    except Exception:
        pass

    try:
        Pets = apps.get_model("pets", "Pets")
    except LookupError:
        return []

    user_field = _user_field_name(Pets)
    if user_field:
        return Pets.objects.filter(**{user_field: user})
    return Pets.objects.all()


def _redirect_to_list_with_params(params: dict):
    base = reverse("expense_list")
    url = "?" + urlencode(params) if params else ""
    return redirect(f"{base}{url}")


@login_required
def expense_list(request):
    qs = Expense.objects.all()

    user_field = _user_field_name(Expense)
    if user_field:
        qs = qs.filter(**{user_field: request.user})

    if _pet_field_exists(Expense):
        qs = qs.select_related("pet")

    pet = request.GET.get("pet", "").strip()
    category = request.GET.get("category", "").strip()
    q = request.GET.get("q", "").strip()
    start = request.GET.get("start", "").strip()
    end = request.GET.get("end", "").strip()

    if _pet_field_exists(Expense) and pet:
        qs = qs.filter(pet_id=pet)

    if category:
        qs = qs.filter(category=category)

    if start:
        d = parse_date(start)
        if d:
            qs = qs.filter(date__gte=d)
    if end:
        d = parse_date(end)
        if d:
            qs = qs.filter(date__lte=d)

    if q:
        text_fields = _safe_text_fields(
            Expense,
            ["name", "notes", "note", "title", "description", "memo", "merchant", "item"],
        )
        q_obj = Q()
        for f in text_fields:
            q_obj |= Q(**{f"{f}__icontains": q})

        if any(f.name == "category" for f in Expense._meta.fields):
            q_obj |= Q(category__icontains=q)

        if _pet_field_exists(Expense):
            q_obj |= Q(pet__name__icontains=q)

        qs = qs.filter(q_obj)

    qs = qs.order_by("-date", "-id")

    total_amount = qs.aggregate(total=Sum("amount"))["total"]

    context = {
        "expenses": qs,
        "pets": _get_user_pets(request.user),
        "categories": getattr(Expense, "CATEGORY_CHOICES", []),
        "pet": pet,
        "category": category,
        "q": q,
        "start": start,
        "end": end,
        "total_amount": total_amount,
    }
    return render(request, "expenses/expense_list.html", context)


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            user_field = _user_field_name(Expense)
            if user_field:
                setattr(obj, user_field, request.user)

            obj.save()
            form.save_m2m()
            return redirect("expense_list")
    else:
        form = ExpenseForm()

    return render(request, "expenses/expense_form.html", {"form": form, "mode": "create"})


@login_required
def expense_update(request, pk):
    obj = get_object_or_404(Expense, pk=pk)

    user_field = _user_field_name(Expense)
    if user_field and getattr(obj, user_field + "_id") != request.user.id:
        return redirect("expense_list")

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=obj)

    return render(
        request,
        "expenses/expense_form.html",
        {"form": form, "mode": "update", "object": obj},
    )


@login_required
def expense_delete(request, pk):
    obj = get_object_or_404(Expense, pk=pk)

    user_field = _user_field_name(Expense)
    if user_field and getattr(obj, user_field + "_id") != request.user.id:
        return redirect("expense_list")

    if request.method == "POST":
        obj.delete()
        return redirect("expense_list")

    return render(request, "expenses/expense_confirm_delete.html", {"object": obj})

@login_required
def filter_by_date(request):
    start = (request.POST.get("start") or request.GET.get("start") or "").strip()
    end = (request.POST.get("end") or request.GET.get("end") or "").strip()

    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end

    return _redirect_to_list_with_params(params)


@login_required
def filter_by_category(request):
    category = (request.POST.get("category") or request.GET.get("category") or "").strip()
    params = {"category": category} if category else {}
    return _redirect_to_list_with_params(params)
