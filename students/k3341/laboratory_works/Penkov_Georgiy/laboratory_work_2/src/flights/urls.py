from django.urls import path

from flights import views

urlpatterns = [
    path("", views.FlightListView.as_view(), name="flight-list"),
    path("<int:pk>/", views.flight_detail_view, name="flight-detail"),
    path("<int:flight_id>/reserve-seat", views.reserve_seat, name="reserve-seat"),
    path("my-registrations", views.my_registrations, name="my-registrations"),
    path(
        "<int:flight_id>/delete-registration",
        views.delete_registration,
        name="delete-registration",
    ),
    path("<int:flight_id>/leave-feedback", views.leave_feedback, name="leave-feedback"),
]
