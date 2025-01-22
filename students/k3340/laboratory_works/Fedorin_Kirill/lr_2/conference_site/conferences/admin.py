from django.contrib import admin

from .models import Conference, Location, ParticipationCondition, PresentationResult, Registration, Review


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date')
    search_fields = ('title', 'topics')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'registered_on')
    search_fields = ('user__username', 'conference__title')

@admin.register(PresentationResult)
class PresentationResultAdmin(admin.ModelAdmin):
    list_display = ('registration', 'is_recommended_for_publication')
    list_filter = ('is_recommended_for_publication',)
