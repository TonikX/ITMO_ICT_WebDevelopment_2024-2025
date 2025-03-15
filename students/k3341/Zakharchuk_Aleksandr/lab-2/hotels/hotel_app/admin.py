from django.contrib import admin

from hotel_app import models

admin.site.register(models.Hotel)
admin.site.register(models.RoomType)
admin.site.register(models.Room)
admin.site.register(models.Reservation)
admin.site.register(models.Review)
