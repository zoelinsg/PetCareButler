from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import PhotoForm
from .models import Photo

@login_required
def upload_photos(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.author = request.user
            photo.save()
            return redirect("photo_list")
    else:
        form = PhotoForm()

    return render(request, "photos/upload_photos.html", {"form": form})


class PhotoListView(LoginRequiredMixin, ListView):
    model = Photo
    template_name = "photos/photo_list.html"
    context_object_name = "photos"

    def get_queryset(self):
        qs = Photo.objects.filter(author=self.request.user)

        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(location__icontains=q)
            ).distinct()

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        return ctx


class PhotoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Photo
    template_name = "photos/photo_detail.html"
    context_object_name = "photo"

    def test_func(self):
        return self.get_object().author == self.request.user


class PhotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Photo
    form_class = PhotoForm
    template_name = "photos/photo_edit.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("photo_detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class PhotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Photo
    template_name = "photos/photo_delete.html"
    success_url = reverse_lazy("photo_list")

    def test_func(self):
        return self.get_object().author == self.request.user
