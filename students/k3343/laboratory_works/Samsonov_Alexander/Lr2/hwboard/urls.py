from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RootView, RegisterStudentView, LoginStudentView, StudentView, LogoutAccountView

urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('account/', StudentView.as_view(), name='account'),
    path('account/register/', RegisterStudentView.as_view(), name='register'),
    path('account/login/', LoginStudentView.as_view(), name='login'),
    path('account/logout/', LogoutAccountView.as_view(), name='logout'),
]
