from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('homeworks/', views.homework_list, name='homework_list'),
    path('submit_hw/<int:hw_id>/', views.submit_hw, name='submit_hw'),
    path('submissions/', views.submissions_list, name='submissions_list'),
    path('success/', views.success_view, name='success_view'),
    path('wrong_role/', views.wrong_role_view, name='wrong_role_view'),
]
