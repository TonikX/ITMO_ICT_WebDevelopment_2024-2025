from django.contrib import admin
from .models import Flight, Reservation, Comment

admin.site.register(Flight)
admin.site.register(Reservation)
admin.site.register(Comment)

