from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff',)


admin.site.register(User, UserAdmin)
admin.site.register(Flight)
admin.site.register(Seat)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(Passenger)
