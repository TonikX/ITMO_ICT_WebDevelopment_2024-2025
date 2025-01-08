from django.urls import path
from .views import *


app_name = "warriors"


urlpatterns = [
   path('warriors/', WarriorAPIView.as_view())
    ]