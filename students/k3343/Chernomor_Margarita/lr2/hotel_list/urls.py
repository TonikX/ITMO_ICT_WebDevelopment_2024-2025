from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import DeleteView

from hotel_list.views import RegisterView, IndexView, logout_view, test_view, HotelListView, HotelDetailView, \
    RoomDetailView, create_reservation, BookingsListView, BookingDeleteView, ReviewCreateView, ReservationUpdateView

urlpatterns = [
    path('', IndexView, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/', ), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('hotels/', HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel_details'),

    path('room/<int:pk>/', RoomDetailView.as_view(), name='room_details'),
    path('room/<int:pk>/reserve/', create_reservation, name='reserve-room'),


    path('bookings/', BookingsListView.as_view(), name='bookings'),
    path('bookings/<int:pk>/cancel/', BookingDeleteView.as_view(), name='bookings'),
    path('bookings/<int:pk>/comment/', ReviewCreateView.as_view(), name='comments-create'),
    path('bookings/<int:pk>/edit/', ReservationUpdateView.as_view(), name='bookings-update'),

    path("admin/", admin.site.urls),
]
