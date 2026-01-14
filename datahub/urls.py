from django.urls import path
from . import views

urlpatterns = [
    path("animal-protect-units/", views.animal_protect_units_page, name="animal-protect-units"),
    path("public-shelters/", views.public_shelters_page, name="public-shelters"),
    path("lost-notices/", views.lost_notices_page, name="lost-notices"),
    path("adoptions/", views.adoptions_page, name="adoptions"),
]
