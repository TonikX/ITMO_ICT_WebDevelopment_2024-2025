from django.contrib import admin

from travelCompany.models import TravelAgency, Tour, Reservation, Review, SoldTour

admin.site.register(TravelAgency)
admin.site.register(Tour)
admin.site.register(Reservation)
admin.site.register(Review)
admin.site.register(SoldTour)