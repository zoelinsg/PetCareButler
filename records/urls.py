from django.urls import path
from . import views

urlpatterns = [
    path("", views.DailyRecordListView.as_view(), name="care_record_list"),
    path("new/", views.DailyRecordCreateView.as_view(), name="care_record_create"),
    path("pet/<int:pet_id>/", views.DailyRecordListView.as_view(), name="care_record_list_by_pet"),
    path("pet/<int:pet_id>/new/", views.DailyRecordCreateView.as_view(), name="care_record_create_by_pet"),
    path("<int:pk>/", views.DailyRecordDetailView.as_view(), name="care_record_detail"),
    path("<int:pk>/edit/", views.DailyRecordUpdateView.as_view(), name="care_record_update"),
    path("<int:pk>/delete/", views.DailyRecordDeleteView.as_view(), name="care_record_delete"),
]
