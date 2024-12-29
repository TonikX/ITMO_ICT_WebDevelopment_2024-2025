from django.contrib import admin

from auth_app.models import HotelAdmin


@admin.register(HotelAdmin)
class HotelAdminAdmin(admin.ModelAdmin): ...
