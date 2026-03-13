from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:room_id>/book/', views.BookingCreateView.as_view(), name='booking_create'),
    path('my/', views.UserBookingListView.as_view(), name='user_bookings'),
    path('<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
]