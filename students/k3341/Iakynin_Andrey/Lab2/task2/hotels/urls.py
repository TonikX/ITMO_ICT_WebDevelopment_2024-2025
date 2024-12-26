from django.urls import path
from . import views
from .views import LogoutView, BookingDeleteView, BookingUpdateView

urlpatterns = [
    path('', views.main, name='main'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('hotels/<int:hotel_id>/', views.hotel_rooms, name='hotel_rooms'),
    path('rooms/<int:room_id>/', views.room_detail, name='rooms_detail'),
    path('rooms/<int:room_id>/booking/', views.booking_room, name='booking_room'),
    path('rooms/<int:pk>/delete/', BookingDeleteView.as_view(), name='reservations_delete'),
    path('rooms/<int:pk>/update/', BookingUpdateView.as_view(), name='reservations_update'),
    path('last_month_bookings/', views.last_month_guests, name='bookings'),
    path('check_out_user/<int:booking_id>/', views.check_out_user, name='check_out_user'),
    path('add_hotel/', views.add_hotel, name='add_hotel'),
    path('add_room/<int:hotel_id>/', views.add_room, name='add_room'),
    path('hotel/delete/<int:hotel_id>/', views.delete_hotel, name='delete_hotel'),
    path('hotel/<int:hotel_id>/room/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('rooms/<int:room_id>/reviews/', views.room_reviews, name='room_reviews'),
]
