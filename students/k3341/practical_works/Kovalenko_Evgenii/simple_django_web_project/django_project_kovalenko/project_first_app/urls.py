from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Пользователи
    path('users/', views.users_list, name='users_list'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),

    # Автомобили
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view(), name='car_update'),
    path('cars/create/', views.CarCreateView.as_view(), name='car_create'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),

    # Главная страница
    path('', views.users_list, name='home'),
]