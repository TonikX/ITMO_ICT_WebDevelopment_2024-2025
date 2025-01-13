from django.urls import path 
from . import views

urlpatterns = [
    path('owners/<int:id>/', views.owner_info),
]