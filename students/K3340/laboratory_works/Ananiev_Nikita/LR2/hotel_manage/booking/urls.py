from django.urls import path

from . import views

urlpatterns = [
    path('add_booking/<int:room_id>', views.CreateBookingView.as_view(), name='add_booking'),
    path('my_bookings/', views.ListBookingView.as_view(), name='my_bookings'),
    path('my_bookings/delete/<int:pk>', views.delete_booking, name='delete_booking'),
    path('my_bookings/update/<int:pk>', views.UpdateBookingView.as_view(), name='update_booking'),
]
