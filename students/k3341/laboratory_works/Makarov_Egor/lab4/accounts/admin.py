from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "full_name", "organization")
    list_filter = ("role",)
    search_fields = ("user__username", "full_name", "organization")
