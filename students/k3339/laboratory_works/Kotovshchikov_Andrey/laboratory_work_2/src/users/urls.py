from django.urls import path

from users import views

urlpatterns = [
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path("sign-in/", views.SignInView.as_view(), name="sign-in"),
    path("sign-out/", views.sign_out, name="sign-out"),
]
