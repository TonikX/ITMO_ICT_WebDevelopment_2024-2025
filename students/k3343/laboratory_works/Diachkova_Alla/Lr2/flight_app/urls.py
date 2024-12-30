from django.urls import path
from . import views

urlpatterns = [
    path('', views.Flights.as_view(), name='flights'),
    path('flight/<str:pk>/', views.FlightInfoView.as_view(), name='flight_info'),
    path('flight/<str:pk>/book/', views.make_booking, name='make_booking'),
    path('bookings/', views.bookings, name='bookings'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking_delete'),
    path('booking/<int:booking_id>/review/', views.review_create, name='review_create'),
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
