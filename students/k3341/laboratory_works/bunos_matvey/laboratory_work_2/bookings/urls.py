from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/rooms/', views.room_list, name='room_list'),
    path('room_type/<int:room_type_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reservation/<int:reservation_id>/edit/', views.edit_reservation, name='edit_reservation'),
    path('reservation/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
    path('reservation/<int:reservation_id>/review/', views.add_review, name='add_review'),
    path('guests/', views.guest_list, name='guest_list'),
]
