from django.urls import path
from .views import RegisterView, UserDetailView, UserUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('user/update/<str:username>/', UserUpdateView.as_view(), name='user-detail'),
    path('user/<str:username>/', UserDetailView.as_view(), name='get-user'),
]