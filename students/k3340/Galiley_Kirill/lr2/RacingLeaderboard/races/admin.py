from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Team, Driver, Car, Race, RaceResult, Comment, Registration

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('bio', 'avatar')}),
    )

class CarInline(admin.TabularInline):
    model = Car
    extra = 1

class DriverAdmin(admin.ModelAdmin):
    inlines = [CarInline]
    list_display = ('user', 'team', 'experience', 'driver_class')
    list_filter = ('experience', 'driver_class', 'team')

class RaceResultInline(admin.TabularInline):
    model = RaceResult
    extra = 1

class RaceAdmin(admin.ModelAdmin):
    inlines = [RaceResultInline]
    list_display = ('name', 'date', 'location')
    list_filter = ('date', 'location')
    search_fields = ('name', 'location', 'description')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'race', 'rating', 'comment_type', 'race_date')
    list_filter = ('comment_type', 'rating', 'race_date')
    search_fields = ('author__username', 'text')

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('driver', 'race', 'registered_at')
    list_filter = ('race', 'registered_at')
    search_fields = ('driver__user__username', 'race__name')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Car)
admin.site.register(Race, RaceAdmin)
admin.site.register(RaceResult)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Registration, RegistrationAdmin)
