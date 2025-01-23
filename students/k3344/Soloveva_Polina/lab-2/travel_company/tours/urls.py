from django.urls import path
from . import views
from .views import BookingDeleteView, BookingUpdateView, BookingDetailView, logout_view, login_view

urlpatterns = [
    # Аутентификация
    path('register/', views.register, name='register'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Туры
    path('tours/', views.tour_list, name='tour_list'),
    path('tours/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tours/<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('tours/<int:pk>/add_review/', views.add_review, name='add_review'),

    # Бронирования
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('my_bookings/<int:pk>/edit', BookingUpdateView.as_view(), name='edit_booking'),
    path('my_bookings/<int:pk>/delete', BookingDeleteView.as_view(), name='delete_booking'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),

    # Админ
    path('add_tour/', views.add_tour, name='add_tour'),
    path('edit_tour/<int:pk>/', views.edit_tour, name='edit_tour'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('confirm_booking/<int:pk>/', views.confirm_booking, name='confirm_booking'),
    path('tour_sales_statistics/', views.sold_tours_by_country, name='tour_sales_statistics'),
]
