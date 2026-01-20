from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_select_related = ("pet", "owner")
    list_display = ("date", "name", "category", "amount", "pet", "owner", "created_at")
    list_filter = ("category", "date")
    search_fields = ("name", "notes", "pet__name", "owner__username")
    ordering = ("-date", "-id")
