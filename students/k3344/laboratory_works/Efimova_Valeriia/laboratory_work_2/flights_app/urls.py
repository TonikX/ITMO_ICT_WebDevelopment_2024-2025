from django.urls import path
from . import views

urlpatterns = [
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('flight/<str:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    path('flight/<str:pk>/book/', views.make_booking, name='make_booking'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('booking/<int:booking_id>/review/', views.review_create, name='review_create'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
