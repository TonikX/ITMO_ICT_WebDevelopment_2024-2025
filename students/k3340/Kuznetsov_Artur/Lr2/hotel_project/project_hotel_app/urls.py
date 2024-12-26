from django.urls import path
from . import views

urlpatterns = [
    # Пользовательские пути
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Отели
    path('', views.HotelListView.as_view(), name='hotel_list'),

    # Номера
    path('hotels/<int:hotel_id>/rooms/', views.get_room_list, name='room_list'),

    # Бронирования
    path('reservations/', views.ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='update_reservation'),
    path('reservations/<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='delete_reservation'),
    path('rooms/<int:room_id>/reserve/', views.create_reservation, name='create_reservation'),

    # Отзывы
    path('rooms/<int:room_id>/reviews/', views.get_room_reviews, name='room_reviews'),
    path('reservations/<int:reservation_id>/reviews/add/', views.create_review, name='create_review'),
]
