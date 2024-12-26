from django.contrib.auth.views import LogoutView
from django.urls import path

from hotelProject import settings
from project_hotel_app import views
from project_hotel_app.views import HotelListView, ReservationDeleteView, ReservationUpdateView

urlpatterns = [
    path('hotels/<int:hotel_id>/rooms/', views.hotel_rooms, name='hotel_rooms'),
    path('rooms/<int:room_id>/reserve/', views.create_reservation, name='reserve_room'),
    path('rooms/<int:room_id>/reviews/', views.room_reviews, name='room_reviews'),
    path('hotels/', HotelListView.as_view(), name = 'hotels'),
    path('register/', views.register, name = 'register'),
    path('login/', views.login, name = 'login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name = 'logout'),
    path('reservations/', views.user_reservations, name='reservations'),
    path('reservations/<int:reservation_id>/review', views.create_review, name='create_review'),
    path('reservations/<int:pk>/update/', ReservationUpdateView.as_view(), name = 'reservation_update'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),
    path('сlients/month/', views.month_clients, name='month_users'),
]