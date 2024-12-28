from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.CreateAccount.as_view(), name="register_account"),
    path("register/admin/", views.AdminCreateView.as_view(), name="register_admin"),
    path("login/", views.account_login, name="login"),
    path("logout/", views.account_logout, name="logout"),
]
