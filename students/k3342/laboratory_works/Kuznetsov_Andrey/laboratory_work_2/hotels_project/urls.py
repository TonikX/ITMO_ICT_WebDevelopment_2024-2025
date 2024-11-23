from django.urls import path
from . import views

urlpatterns = [
    path("", views.HotelListView.as_view(), name="hotel_list"),
    path("hotel/<int:pk>/", views.HotelDetailView.as_view(), name="hotel_detail"),
    path("room/<int:room_id>/reserve/", views.reserve_room, name="reserve_room"),
    path("reservations/", views.reservation_list, name="reservation_list"),
    path("reservation/<int:reservation_id>/edit/", views.edit_reservation, name="edit_reservation"),
    path("reservation/<int:reservation_id>/delete/", views.delete_reservation, name="delete_reservation"),
    path("room/<int:room_id>/review/", views.add_review, name="add_review"),
    path("recent-guests/", views.recent_guests, name="recent_guests"),
]
