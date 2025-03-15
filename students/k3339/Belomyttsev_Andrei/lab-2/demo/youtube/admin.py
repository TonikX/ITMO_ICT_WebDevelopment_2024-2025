from django.contrib import admin

from .models import Channel, Review

class ChannelAdmin(admin.ModelAdmin):
  list_display = ('title', 'user', 'is_approved', 'time_create')
  ordering = ('-time_create', 'title')
  list_editable = ('is_approved',)

class ReviewAdmin(admin.ModelAdmin):
  list_display = ('channel', 'user', 'rating', 'time_create')
  list_display_links = ('channel', 'user')
  ordering = ('-time_create', 'channel')

admin.site.register(Channel, ChannelAdmin)
admin.site.register(Review, ReviewAdmin)