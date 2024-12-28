from django.urls import path
from .views import *


app_name = "hotel_api"

urlpatterns = [
    path('rooms/<int:id>/', RoomAPIView.as_view(), name='get_room'),
    path('rooms/<int:id>/update', RoomUpdateAPIView.as_view(), name='update_room'),
    path('rooms/list/', RoomListAPIView.as_view(), name='get_room_list'),
    path('rooms/room_types/', RoomTypeListAPIView.as_view(), name='get_room_type_list'),
]