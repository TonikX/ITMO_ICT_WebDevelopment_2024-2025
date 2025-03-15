from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('rooms/<int:room_id>/reviews/', views.room_reviews, name='room_reviews'),
    path('rooms/<int:room_id>/book/', views.book_room, name='book_room'),
    path('reservations/<int:reservation_id>/review/', views.write_review, name='write_review'),
    path('user_bookings/', views.user_bookings, name='user_bookings'),
    path('monthly_clients/', views.monthly_clients, name='monthly_clients'),
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('reservations/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('reservations/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
]