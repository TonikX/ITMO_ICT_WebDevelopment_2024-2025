from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('booking/create/<int:room_id>/', views.booking_create, name='booking_create'),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('accounts/register/', views.register, name='register'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('bookings/', views.UserBookingsListView.as_view(), name='user_bookings'),
    path('recent-guests/', views.RecentGuestsListView.as_view(), name='recent_guests'),
    path('bookings/', views.UserBookingsListView.as_view(), name='user_bookings'),
    path('booking/<int:pk>/edit/', views.booking_edit, name='booking_edit'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('room/<int:room_id>/reviews/', views.room_review, name='room_review'),



]
