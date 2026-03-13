from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hotels.urls')),
    path('users/', include('users.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
]