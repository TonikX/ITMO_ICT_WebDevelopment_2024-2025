from django.contrib import admin

from rooms.models import RoomType, Room, Floor

# Register your models here.
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Floor)