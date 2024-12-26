from django.contrib import admin
from .models import Hotel, RoomType, Room, Reservation, Review, Guest, Booking
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )

admin.site.register(User, CustomUserAdmin)

# Регистрация моделей в админ-панели
admin.site.register(Guest)
admin.site.register(Hotel)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Booking)
