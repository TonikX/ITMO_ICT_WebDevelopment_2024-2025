from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("pets_in_departs", CountPetsInDepartAPIView.as_view()),
    path("pets_in_commun", GetPetsInCommunalAPIView.as_view()),
    path("pets_with/<int:pk>", GetPetsTogetherAPIView.as_view()),
    path("pets", GetPetsAPIView.as_view()),

    path("pet/create", CreatePetAPIView.as_view()),
    path("pet/delete/<int:pk>", DeletePetAPIView.as_view()),
    path("pet/update/<int:pk>", UpdatePetAPIView.as_view()),

    path("valliers_empty", GetEmptyValliersAPIView.as_view()),
    path("pets_rent_in/state", GetPetsStateRent.as_view()),
    path("pets_rent_out/report", GetReportOutRentAPIView.as_view()),

    path("diets", ListDietAPIView.as_view()),
    path("diet/create", CreateDietAPIView.as_view()),
    path("diet/delete/<int:pk>", DeleteDietAPIView.as_view()),
    path("diet/update/<int:pk>", UpdateDietAPIView.as_view()),

    path("habiteds", ListHabitedAPIView.as_view()),
    path("habited/create", CreateHabitedAPIView.as_view()),
    path("habited/delete/<int:pk>", DeleteHabitedAPIView.as_view()),
    path("habited/update/<int:pk>", UpdateHabitedAPIView.as_view()),

    path("products", ListProductAPIView.as_view())
]