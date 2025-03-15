from django.contrib.auth.views import LogoutView
from django.urls import path

from hotel_app import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("reservations/", views.user_reservations, name="reservations"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("", views.root, name="root"),
    path("hotels/", views.HotelListView.as_view(), name="hotels"),
    path("hotels/<int:hotel_id>/rooms/", views.hotel_rooms, name="hotel_rooms"),
    path("rooms/<int:room_id>/reserve/", views.create_reservation, name="create_reservation"),
    path("reservations/<int:pk>/update/", views.UpdateReservationView.as_view(), name="update_reservation"),
    path("reservations/<int:pk>/delete/", views.DeleteReservationView.as_view(), name="delete_reservation"),
    path("reservations/<int:reservation_id>/review", views.create_review, name="create_review"),
    path("rooms/<int:room_id>/reviews/", views.room_reviews, name="room_reviews"),
    path("clients/month/", views.month_clients, name="month_clients"),
]
