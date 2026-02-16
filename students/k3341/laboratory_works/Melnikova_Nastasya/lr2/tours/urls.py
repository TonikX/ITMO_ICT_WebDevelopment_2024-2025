from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная страница — список туров
    path('', views.tour_list, name='tour_list'),

    # Регистрация и вход
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tours/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Бронирования
    path('reserve/<int:tour_id>/', views.reserve_tour, name='reserve_tour'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('delete_reservation/<int:res_id>/', views.delete_reservation, name='delete_reservation'),

    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('sold_tours/', views.sold_tours, name='sold_tours'),
]


