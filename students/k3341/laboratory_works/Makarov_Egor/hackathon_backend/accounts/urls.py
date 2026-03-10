from django.urls import path
from .views import MyProfileView

urlpatterns = [
    path("profiles/me/", MyProfileView.as_view(), name="my-profile"),
]
