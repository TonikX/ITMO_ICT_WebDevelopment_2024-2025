from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),

    path('hotels/', views.HotelListView.as_view(), name='hotels'),
    path('<int:hotel_id>/', views.rooms_list, name='rooms'),
    path('<int:hotel_id>/<int:room_id>/book_room', views.book_room, name='book_room'),
    path('<int:hotel_id>/<int:room_id>/reviews', views.room_reviews, name='room_reviews'),
    path('<int:hotel_id>/monthly/', views.monthly_clients, name='monthly_clients'),

    path('bookings/', views.user_bookings, name='bookings'),
    path('bookings/<int:booking_id>/write_review', views.write_review,
         name='write_review'),
    path('bookings/<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
]
