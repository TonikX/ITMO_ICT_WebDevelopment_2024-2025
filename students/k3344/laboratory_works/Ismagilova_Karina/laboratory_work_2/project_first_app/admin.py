from django.contrib import admin
from .models import User, Conference, Review, Participant, Results

admin.site.register(User)
admin.site.register(Conference)
admin.site.register(Review)
admin.site.register(Participant)
admin.site.register(Results)
