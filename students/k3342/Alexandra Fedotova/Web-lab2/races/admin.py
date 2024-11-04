from django.contrib import admin
from .models import Team, Participant, Race, Registration, Comment, RaceResult

admin.site.register(Team)
admin.site.register(Participant)
admin.site.register(Race)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(RaceResult)
