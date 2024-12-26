from django.contrib import admin

from .models import User, Tour, Review, Reservation, CountrySales

admin.site.register(User)
admin.site.register(Tour)
admin.site.register(Review)
admin.site.register(Reservation)
admin.site.register(CountrySales)

