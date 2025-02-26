from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotel/<int:hotel_id>/rooms/', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:room_id>/booking/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('room/<int:room_id>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('bookings/', views.BookingListView.as_view(), name='bookings_list'),
    path('monthly-guests/', views.MonthlyGuestListView.as_view(), name='monthly_guests'),
]