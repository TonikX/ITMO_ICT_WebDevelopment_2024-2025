from django.urls import path
from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
]