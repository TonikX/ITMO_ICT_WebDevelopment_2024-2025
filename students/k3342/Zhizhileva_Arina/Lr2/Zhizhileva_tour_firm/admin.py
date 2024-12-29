from django.contrib import admin
from .models import TourAgency, Tour, Booking, Review
# Register your models here.


admin.site.register(TourAgency)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Review)