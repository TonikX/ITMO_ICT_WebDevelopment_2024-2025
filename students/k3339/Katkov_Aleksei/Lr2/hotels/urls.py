from django.urls import path
from .views import create_booking
from . import views
from .views import admin_bookings

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'),
    path('room/<int:room_id>/book/', create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-guests/', views.last_month_guests, name='last_month_guests'),
    path("admin-bookings/", admin_bookings, name="admin_bookings"),

]
