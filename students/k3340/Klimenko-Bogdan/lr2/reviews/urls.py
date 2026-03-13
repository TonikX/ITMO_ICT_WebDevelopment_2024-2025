from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('room/<int:room_id>/add/', views.ReviewCreateView.as_view(), name='review_create'),
]