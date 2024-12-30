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

    def delete_model(self, request, obj):
        # Ensure reviews are deleted before the booking
        Review.objects.filter(booking=obj).delete()
        obj.delete()

    def save_model(self, request, obj, form, change):
        # Custom logic for saving the booking (if needed)
        super().save_model(request, obj, form, change)


class ReviewAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Delete review and ensure foreign key constraints are respected
        obj.delete()


admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Flight)
