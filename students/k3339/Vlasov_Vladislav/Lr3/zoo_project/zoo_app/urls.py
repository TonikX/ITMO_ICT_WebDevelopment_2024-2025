from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("pets_in_departs", CountPetsInDepartAPIView.as_view()),
    path("pets_in_commun", GetPetsInCommunalAPIView.as_view()),
    path("pets_with/<int:pk>", GetPetsTogetherAPIView.as_view()),
    path("pets", GetPetsAPIView.as_view()),
    path("pet/create", CreatePetAPIView.as_view()),
    path("valliers_empty", GetEmptyValliersAPIView.as_view()),
    path("pets_rent_in/state", GetPetsStateRent.as_view()),
    path("pets_rent_out/report", GetReportOutRentAPIView.as_view()),
]