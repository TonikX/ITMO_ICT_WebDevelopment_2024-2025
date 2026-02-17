from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from racing_app import views as racing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('racing_app.urls')),
    path('register/', racing_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='racing_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]