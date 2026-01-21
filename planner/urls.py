from django.urls import path
from . import views

urlpatterns = [
    path("", views.month_view, name="month"),
    path("day/<int:year>/<int:month>/<int:day>/", views.day_view, name="day"),
    path("create/", views.event_create, name="create"),
    path("<int:pk>/", views.event_detail, name="detail"),
    path("<int:pk>/edit/", views.event_update, name="update"),
    path("<int:pk>/delete/", views.event_delete, name="delete"),
    path("reminders/", views.reminder_list, name="planner_reminders"),
    path("reminders/mark-all/", views.reminder_mark_all, name="planner_reminders_mark_all"),
]
