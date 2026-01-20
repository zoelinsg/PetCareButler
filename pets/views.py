from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, UpdateView, DeleteView
from .forms import PetsForm
from .models import Pets

class PetsListView(LoginRequiredMixin, ListView):
    model = Pets
    template_name = "pets/pets_list.html"
    context_object_name = "pets"
    paginate_by = 24

    def get_queryset(self):
        qs = Pets.objects.filter(owner=self.request.user)

        status = self.request.GET.get("status", "alive")
        if status == "alive":
            qs = qs.filter(is_deceased=False)
        elif status == "deceased":
            qs = qs.filter(is_deceased=True)
        elif status == "all":
            pass

        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(breed__icontains=q)
                | Q(pet_chip__icontains=q)
                | Q(features__icontains=q)
            )

        return qs.order_by("-updated_at", "-id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        ctx["status"] = self.request.GET.get("status", "alive")
        return ctx


class PetsDetailView(LoginRequiredMixin, DetailView):
    model = Pets
    template_name = "pets/pets_detail.html"
    context_object_name = "pet"

    def get_queryset(self):
        return Pets.objects.filter(owner=self.request.user)


@login_required
def pets_add(request):
    if request.method == "POST":
        form = PetsForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect("pets_detail", pk=pet.pk)
    else:
        form = PetsForm()

    return render(request, "pets/pets_add.html", {"form": form})


class PetsUpdateView(LoginRequiredMixin, UpdateView):
    model = Pets
    form_class = PetsForm

    template_name = "pets/pets_edit.html"

    def get_queryset(self):
        return Pets.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return redirect("pets_detail", pk=self.object.pk).url


class PetsDeleteView(LoginRequiredMixin, DeleteView):
    model = Pets
    template_name = "pets/pets_delete.html"

    def get_queryset(self):
        return Pets.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return redirect("pets_list").url
