from django.urls import path
from .views import *


app_name = "auth_api"

urlpatterns = [
    path("users/<int:id>/", UserAPIView.as_view(), name="get_client"),
    path("users/list/", UserListAPIView.as_view(), name="get_client_list"),
    path("users/<int:id>/update", UserUpdateAPIView.as_view(), name="update_client"),
]