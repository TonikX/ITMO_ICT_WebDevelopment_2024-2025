from django.contrib import admin

from raceboard.models import Participant, Race, RaceResult, Comment, Registration

# Register your models here.
admin.site.register(Participant)
admin.site.register(Race)
admin.site.register(RaceResult)
admin.site.register(Registration)
admin.site.register(Comment)