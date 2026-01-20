from django.contrib import admin
from .models import Pets

@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "species",
        "gender",
        "is_neutered",
        "is_deceased",
        "pet_chip",
    )
    list_filter = ("species", "gender", "is_neutered", "is_deceased")
    search_fields = ("name", "breed", "pet_chip", "owner__username")
