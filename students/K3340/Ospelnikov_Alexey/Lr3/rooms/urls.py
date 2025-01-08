from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from . import views
from .serializers import RoomTypeSerializer

from .views import RoomTypeViewSet, RoomViewSet, FloorViewSet

router = routers.DefaultRouter()
router.register(r'roomtypes', RoomTypeViewSet)
router.register(r'rooms_admin', RoomViewSet)

router.register(r'floors', FloorViewSet)
urlpatterns = [

    path('', include(router.urls)),
    path('get_rooms/', views.get_rooms),
    path('get_empty_rooms/', views.get_empty_rooms),

    #gets all user profiles and create a new profile
   # retrieves profile details of the currently logged in user
]