from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('flight/<int:flight_id>/', views.flight_details, name='flight_details'),
    path('flight/<int:flight_id>/reserve/', views.reserve_seat, name='reserve_seat'),
    path('flight/<int:flight_id>/review/', views.add_review, name='add_review'),
    path('my-reservations/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
]
