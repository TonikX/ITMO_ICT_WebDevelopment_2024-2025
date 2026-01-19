from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RacingUser, Team, Car, Racer, Race, RaceRegistration, RaceResult, Comment


@admin.register(RacingUser)
class RacingUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'experience_years']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'experience_years', 'phone', 'date_of_birth')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('bio', 'experience_years', 'phone', 'date_of_birth')
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_date', 'racer_count']
    list_filter = ['country', 'founded_date']
    search_fields = ['name', 'country']

    def racer_count(self, obj):
        return obj.racer_set.count()

    racer_count.short_description = 'Кол-во гонщиков'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'team', 'car_class', 'horsepower']
    list_filter = ['car_class', 'team']
    search_fields = ['model']

@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'racer_class', 'wins_count']
    list_filter = ['racer_class', 'team']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'race_type', 'location', 'start_date', 'is_active']
    list_filter = ['race_type', 'is_active', 'start_date']
    search_fields = ['name', 'location']

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ['racer', 'race', 'car', 'registration_date', 'is_confirmed']
    list_filter = ['is_confirmed', 'race']
    search_fields = ['racer__user__first_name', 'racer__user__last_name']

@admin.register(RaceResult)
class RaceResultAdmin(admin.ModelAdmin):
    list_display = ['race_registration', 'position', 'points', 'dnf']
    list_filter = ['dnf', 'position']
    search_fields = ['race_registration__racer__user__first_name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'race', 'comment_type', 'rating', 'comment_date']
    list_filter = ['comment_type', 'rating']
    search_fields = ['author__username', 'race__name']