from django.contrib import admin
from .models import User, Flight, Booking, Review
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('passport_number', 'full_name', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('passport_number', 'password')}),
        ('Персональная информация', {'fields': ('full_name',)}),
        ('Права доступа', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {'fields': ('passport_number', 'full_name', 'password1', 'password2')}),
    )
    search_fields = ('passport_number', 'full_name')
    ordering = ('passport_number',)
    filter_horizontal = ('groups', 'user_permissions',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_number', 'user', 'flight', 'ticket_number')
    list_filter = ('flight',)
    search_fields = ('booking_number', 'user__full_name', 'flight__flight_number')
    ordering = ('booking_number',)

admin.site.register(User, UserAdmin)
admin.site.register(Flight)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review)
