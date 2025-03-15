# conferences/admin.py
from django.contrib import admin
from .models import Conference, AuthorRegistration, Review

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'location', 'recommended_for_publication')
    list_filter = ('recommended_for_publication',)

@admin.register(AuthorRegistration)
class AuthorRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'registration_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'rating', 'comment_date')
