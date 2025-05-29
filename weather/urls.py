from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("autocomplete/", views.autocomplete_city, name="autocomplete_city"),
]
