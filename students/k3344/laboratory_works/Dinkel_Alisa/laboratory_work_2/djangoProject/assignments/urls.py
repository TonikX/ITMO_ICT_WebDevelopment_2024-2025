from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.redirect_to_login, name='home_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Для клиентской части
    path('register/', views.register, name='register'),
    path('assignments/', views.AssignmentListView.as_view(), name='assignment_list'),
    path('submit/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
]
