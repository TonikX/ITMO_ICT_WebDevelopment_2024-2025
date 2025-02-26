from django.contrib import admin
from .models import Conference, Author, Presentation, Review, Registration

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'start_date', 'end_date')
    search_fields = ('title', 'venue')
    list_filter = ('start_date', 'end_date')
    ordering = ('start_date',)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'biography')
    search_fields = ('user__username', 'user__email')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'date_registered', 'title')
    list_filter = ('conference',)
    search_fields = ('user__username', 'conference__title')
    raw_id_fields = ('user', 'conference')

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'conference', 'author', 'recommended_for_publication')
    search_fields = ('title', 'conference__title', 'author__user__username')
    list_filter = ('recommended_for_publication', 'conference')
    ordering = ('conference', 'author')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('conference', 'author', 'rating', 'comment_date')
    search_fields = ('conference__title', 'author__username', 'text')
    list_filter = ('rating', 'comment_date')
    ordering = ('comment_date', 'rating')