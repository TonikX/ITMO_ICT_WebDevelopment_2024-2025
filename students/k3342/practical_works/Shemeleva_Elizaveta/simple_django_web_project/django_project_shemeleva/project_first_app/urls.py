from django.urls import path
from . import views
from .views import CarListView, CarDetailView, CarUpdateView, register
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/', views.users_list, name='users_list'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project_first_app/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('add_car/', views.add_car, name='add_car'),
    path('my_cars/', views.user_cars, name='user_cars'),

]
