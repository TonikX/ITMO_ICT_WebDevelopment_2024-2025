from django.urls import path
from . import views
from .views import CarCreateView, CarUpdateView, CarDeleteView, CarListView, CarDetailView

urlpatterns = [
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/', views.users_list, name='users_list'),
    path('user/add/', views.UserCreateView.as_view(), name='user_add'),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('cars/', CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('car/add/', CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
]
