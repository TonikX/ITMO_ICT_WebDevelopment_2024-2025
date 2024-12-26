from django.urls import path

from hotel_app import views

urlpatterns = [
    path(
        "employees/",
        view=views.EmployeeView.as_view(),
    ),
    path(
        "employees/<int:pk>/",
        view=views.EmployeeDetailView.as_view(),
    ),
    path(
        "employees/<int:employee_pk>/schedule/",
        view=views.EmployeeScheduleCreateView.as_view(),
    ),
    path(
        "employees/<int:employee_pk>/schedule/reset/",
        view=views.EmployeeScheduleResetView.as_view(),
    ),
    path(
        "guests/",
        view=views.GuestView.as_view(),
    ),
    path(
        "guests/<int:pk>/",
        view=views.GuestDetailView.as_view(),
    ),
    path(
        "guests/<int:pk>/overlapping/",
        view=views.GuestOverlappingView.as_view(),
    ),
    path(
        "rooms/",
        view=views.RoomView.as_view(),
    ),
    path(
        "rooms/<int:pk>/booking/",
        view=views.RoomBookingView.as_view(),
    ),
    path(
        "rooms/<int:pk>/guests/",
        view=views.RoomGuestView.as_view(),
    ),
    path(
        "reports/<int:quarter>/",
        view=views.ReportPerQuarterView.as_view(),
    ),
]
