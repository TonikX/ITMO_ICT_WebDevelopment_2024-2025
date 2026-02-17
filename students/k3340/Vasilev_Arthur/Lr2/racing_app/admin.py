from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, Car, Race, RaceRegistration, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('experience', 'driver_class', 'bio')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('experience', 'driver_class', 'bio')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'experience', 'is_staff')
    list_filter = ('experience', 'is_staff', 'is_superuser')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'owner', 'team', 'year')
    list_filter = ('team', 'year')
    search_fields = ('model', 'owner__username')

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('name', 'location')
    date_hierarchy = 'date'

class RaceRegistrationInline(admin.TabularInline):
    model = RaceRegistration
    extra = 1
    readonly_fields = ('registration_date',)

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('race', 'racer', 'position', 'final_time', 'result')
    list_editable = ('position', 'final_time', 'result')
    list_filter = ('race', 'racer')
    search_fields = ('racer__username', 'race__name')
    readonly_fields = ('registration_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'race', 'type', 'rating', 'created_date', 'is_approved')
    list_editable = ('is_approved',)
    list_filter = ('type', 'rating', 'is_approved', 'created_date')
    search_fields = ('author__username', 'race__name', 'text')
    date_hierarchy = 'created_date'