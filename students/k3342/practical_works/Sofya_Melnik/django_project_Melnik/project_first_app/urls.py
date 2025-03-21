from django.urls import path
from . import views

urlpatterns = [
    path('carowner/<int:carowner_id>/', views.carowner_detail, name='carowner_detail')
]