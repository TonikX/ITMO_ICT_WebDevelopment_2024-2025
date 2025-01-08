from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from . import views
from .views import EmployeeViewSet, RoomCleanViewSet

router = routers.DefaultRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'rooms_clean', RoomCleanViewSet)

urlpatterns = [

    path('', include(router.urls)),
    path('get_cleaner_rooms/', views.get_cleaner_rooms),
    #gets all user profiles and create a new profile
   # retrieves profile details of the currently logged in user
]