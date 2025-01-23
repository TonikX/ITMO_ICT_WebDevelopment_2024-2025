# Пропишем маршруты для каждого представления

from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_flights, name="view_flights"),
    path("my/<str:tab>/", views.view_bookings, name="view_bookings"),
    path("flight/<int:flight_id>/book/", views.book_flight, name="book_flight"),
    path("booking/<int:booking_id>/delete/", views.delete_booking, name="delete_booking"),
    path("flight/<int:flight_id>/feedback/", views.give_feedback, name="give_feedback"),
    path("flight/<int:flight_id>/", views.flight_details, name="flight_details"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]