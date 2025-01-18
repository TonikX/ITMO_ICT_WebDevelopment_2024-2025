from django.contrib import admin
from .models import Conference, Review, Participant, PresentationResult, User

admin.site.register(User)
admin.site.register(Conference)
admin.site.register(Review)
admin.site.register(Participant)
admin.site.register(PresentationResult)
