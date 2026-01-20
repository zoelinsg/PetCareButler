from django.urls import path
from . import views

urlpatterns = [
    path("", views.PhotoListView.as_view(), name="photo_list"),
    path("upload/", views.upload_photos, name="upload_photos"),
    path("<int:pk>/", views.PhotoDetailView.as_view(), name="photo_detail"),
    path("<int:pk>/edit/", views.PhotoUpdateView.as_view(), name="photo_edit"),
    path("<int:pk>/delete/", views.PhotoDeleteView.as_view(), name="photo_delete"),
]
