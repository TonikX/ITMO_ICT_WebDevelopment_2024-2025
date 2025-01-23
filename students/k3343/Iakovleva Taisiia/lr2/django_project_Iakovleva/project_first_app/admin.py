from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Flight, Reservation, Review

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('passport', 'birth_date')}),
#     )
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('passport', 'birth_date')}),
#     )

admin.site.register(User)
admin.site.register(Flight)
admin.site.register(Reservation)
admin.site.register(Review)
