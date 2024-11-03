from django.contrib import admin
from .models import *

admin.site.register((User,
                     Participant,
                     Conference,
                     ConferenceAuditor,
                     ConferencePerformance,
                     Review,
                     Commentary))
