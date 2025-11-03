from django.urls import path
from . import views


urlpatterns = [
    path('', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),

    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),

    path('reservations/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('reservations/create/', views.ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/update/', views.ReservationUpdateView.as_view(), name='reservation_update'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),

    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
]