from django.urls import path

from . import views

urlpatterns = [
    path("all", views.hotel_list, name="hotel_list"),
    path("create_hotel/", views.create_hotel, name="create_hotel"),
    path("view_hotel/<int:pk>/", views.view_hotel, name="view_hotel"),
    path("create_room/<int:hotel_pk>/", views.create_room, name="create_room"),
    path("book_room/<int:hotel_pk>/", views.book_room, name="book_room"),
    path("reservation_success/", views.reservation_success, name="reservation_success"),
    path("room/<int:room_id>/add_review/", views.add_review, name="add_review"),
    path("room/<int:room_id>/room_reviews/", views.room_reviews, name="room_reviews"),
]
