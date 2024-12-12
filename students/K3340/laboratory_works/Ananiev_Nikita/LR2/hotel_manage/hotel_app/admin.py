from django.contrib import admin

from .models import *

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(HotelPicture)
admin.site.register(RoomPicture)
