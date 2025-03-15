from django.contrib import admin

from .models import Conference, Registration, Presentation, Review

admin.site.register(Conference)
admin.site.register(Registration)
admin.site.register(Presentation)
admin.site.register(Review)
