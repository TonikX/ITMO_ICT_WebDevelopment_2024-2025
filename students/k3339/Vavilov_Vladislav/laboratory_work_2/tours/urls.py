from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("sold-tours/", views.sold_tours, name="sold_tours"),
    path(
        "staff/",
        views.staff_dashboard,
        name="staff_dashboard",
    ),

    path(
        "staff/bookings/<int:pk>/confirm/",
        views.confirm_booking,
        name="confirm_booking",
    ),

    path(
        "staff/bookings/<int:pk>/cancel/",
        views.cancel_booking_staff,
        name="cancel_booking_staff",
    ),

    path("", views.tour_list, name="tour_list"),
    path("tour/<int:pk>/", views.tour_detail, name="tour_detail"),

    path("register/", views.register, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html"
        ),
        name="login",
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),

    path(
        "tour/<int:pk>/book/",
        views.create_booking,
        name="create_booking",
    ),

    path(
        "bookings/",
        views.booking_list,
        name="booking_list",
    ),

    path(
        "bookings/<int:pk>/edit/",
        views.edit_booking,
        name="edit_booking",
    ),

    path(
        "bookings/<int:pk>/delete/",
        views.delete_booking,
        name="delete_booking",
    ),

    path(
        "tour/<int:pk>/review/",
        views.create_review,
        name="create_review",
    ),
]
