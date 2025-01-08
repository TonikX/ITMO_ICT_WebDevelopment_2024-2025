from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/create', views.hotel_create, name='hotel-create'),
    path('hotels/update/<int:hotel_id>', views.HotelUpdateView.as_view(), name='hotel-update'),
    path('hotels/delete/<int:hotel_id>', views.HotelDeleteView.as_view(), name='hotel-delete'),
    path('<int:hotel_id>/rooms/', views.hotel_rooms, name='hotel-rooms'),
    path('<int:hotel_id>/rooms/create', views.room_create, name='room-create'),
    path('rooms/update/<int:room_id>', views.RoomUpdateView.as_view(), name='room-update'),
    path('rooms/delete/<int:room_id>', views.RoomDeleteView.as_view(), name='room-delete'),
    path('rooms/', views.rooms, name='rooms'),
    path('bookings/', views.bookings, name='bookings'),
    path('<int:hotel_id>/bookings/', views.hotel_bookings, name='hotel-bookings'),
    path('<int:hotel_id>/bookings/admin-create', views.booking_admin_create, name='booking-admin-create'),
    path('<int:room_id>/bookings/create', views.booking_create, name='booking-create'),
    path('bookings/update/<int:booking_id>', views.BookingUpdateView.as_view(), name='booking-update'),
    path('bookings/delete/<int:booking_id>', views.BookingDeleteView.as_view(), name='booking-delete'),
    path('users/last-month', views.users_last_month, name='users-last-month'),
    path('reviews/<int:room_id>', views.reviews, name='reviews'),
    path('reviews/<int:room_id>/create', views.review_create, name='review-create'),
]