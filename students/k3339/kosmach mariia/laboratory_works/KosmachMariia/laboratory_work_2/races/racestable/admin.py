from django.contrib import admin
from racestable.models import Racer, Race, RaceConnection, Comment, User

admin.site.register(User)
admin.site.register(Racer)
admin.site.register(Race)
admin.site.register(RaceConnection)
admin.site.register(Comment)
