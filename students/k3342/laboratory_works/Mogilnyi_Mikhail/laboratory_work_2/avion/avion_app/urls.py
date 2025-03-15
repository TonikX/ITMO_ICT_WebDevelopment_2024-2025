from django.urls import path
from .views import (
    register, flight_list, reserve_seat,
    edit_reservation, delete_reservation,
    flight_passengers, add_review, profile, home,
    cancel_reservation, flight_reviews
)

urlpatterns = [
    path('', home, name='home'),  # Ensure you have a home view defined
    path('register/', register, name='register'),
    path('flights/', flight_list, name='flight_list'),
    path('flights/<int:flight_id>/reserve/', reserve_seat, name='reserve_seat'),
    path('reservations/<int:reservation_id>/edit/', edit_reservation, name='edit_reservation'),
    path('reservations/<int:reservation_id>/delete/', delete_reservation, name='delete_reservation'),
    path('flights/<int:flight_id>/passengers/', flight_passengers, name='flight_passengers'),
    path('flights/<int:flight_id>/review/', add_review, name='add_review'),
    path('flights/<int:flight_id>/reviews/', flight_reviews, name='flight_reviews'),
    path('accounts/profile/', profile, name='profile'),
    path('flights/<int:flight_id>/reserve/', reserve_seat, name='reserve_seat'),
    path('reservations/cancel/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
]
