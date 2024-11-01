from django.contrib import admin
from .models import *

admin.site.register((User,
                     Participant,
                     Conference,
                     ConferenceAuditor,
                     ConferenceSpeaker,
                     Review,
                     Commentary))
