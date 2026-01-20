from django.urls import path
from . import views

urlpatterns = [
    path("", views.expense_list, name="expense_list"),
    path("create/", views.expense_create, name="expense_create"),
    path("<int:pk>/edit/", views.expense_update, name="expense_update"),
    path("<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    path("filter-by-date/", views.filter_by_date, name="filter_by_date"),
    path("filter-by-category/", views.filter_by_category, name="filter_by_category"),
]
