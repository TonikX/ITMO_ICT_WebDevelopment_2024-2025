from .views import *
from django.urls import path
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', flight_list, name='flights'),
    path('flight/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('flight/<int:flight_pk>/passengers/', passenger_list, name='passengers'),
    path('flight/<int:flight_pk>/submit_review/', submit_review, name='submit_review'),
    path('flight/<int:flight_pk>/seat/<int:seat_pk>/reserve/', submit_reservation, name='submit_reservation'),
    path('reservation/<int:pk>/edit/', edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', delete_reservation, name='delete_reservation'),
    path('my-reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('register-passenger/<int:reservation_pk>/', register_passenger, name='register_passenger'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
