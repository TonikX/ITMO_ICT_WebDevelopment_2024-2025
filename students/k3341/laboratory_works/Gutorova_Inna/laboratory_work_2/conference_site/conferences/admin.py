from django.contrib import admin
from .models import Conference, Registration, Review, PresentationResult

admin.site.register(Conference)
admin.site.register(Registration)
admin.site.register(Review)
admin.site.register(PresentationResult)
