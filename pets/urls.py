from django.urls import path
from . import views

urlpatterns = [
    path("", views.PetsListView.as_view(), name="pets_list"),
    path("add/", views.pets_add, name="pets_add"),
    path("<int:pk>/", views.PetsDetailView.as_view(), name="pets_detail"),
    path("<int:pk>/edit/", views.PetsUpdateView.as_view(), name="pets_edit"),
    path("<int:pk>/delete/", views.PetsDeleteView.as_view(), name="pets_delete"),
]