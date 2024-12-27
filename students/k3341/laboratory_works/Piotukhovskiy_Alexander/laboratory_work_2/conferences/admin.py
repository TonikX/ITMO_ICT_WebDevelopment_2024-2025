from django.contrib import admin

from .models import Conference, ConferenceRating


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date', 'publication_recommended')
    list_filter = ('publication_recommended', 'start_date', 'end_date')
    search_fields = ('title', 'location')
    ordering = ('start_date',)
    fields = (
        'title', 'topics', 'location', 'start_date', 'end_date', 'description', 'participation_conditions',
        'owner', 'participants', 'publication_recommended'
    )
    filter_horizontal = ('participants',)


@admin.register(ConferenceRating)
class ConferenceRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'rating')
    search_fields = ('user__username', 'conference__title')
