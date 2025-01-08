from django.contrib.auth import views as auth_views
from .views import *
from django.urls import path

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', FlightListView.as_view(), name='flights'),  # flights/
    path('flight/<int:pk>/', FlightDetailView.as_view(), name='flight_detail'),
    path('flight/<int:flight_pk>/reservations/', reservations_list, name='reservations_list'),
    path('flight/<int:flight_pk>/passengers/', passenger_list, name='passengers_list'),
    path('flight/<int:flight_pk>/submit_review/', submit_review, name='submit_review'),
    path('flight/<int:flight_pk>/seat/<int:seat_pk>/reserve/', submit_reservation, name='submit_reservation'),
    path('reservation/<int:pk>/edit/', edit_reservation, name='edit_reservation'),
    path('reservation/<int:pk>/delete/', delete_reservation, name='delete_reservation'),
    path('my-reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('register-passenger/<int:reservation_pk>/', register_passenger, name='register_passenger'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),  # URL for user profile
]
