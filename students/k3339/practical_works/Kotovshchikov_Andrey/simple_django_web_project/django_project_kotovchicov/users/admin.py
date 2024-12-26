from django.contrib import admin
from driving.models import CarOwner
from users.models import User


class CarOwnerInline(admin.TabularInline):
    model = CarOwner
    can_delete = False
    readonly_fields = ("first_name", "last_name", "birthdate")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ("email", "passport_number", "home_address", "nationality")
    inlines = [CarOwnerInline]
