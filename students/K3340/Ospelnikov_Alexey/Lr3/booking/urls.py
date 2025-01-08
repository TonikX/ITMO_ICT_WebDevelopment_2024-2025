from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework import routers

from booking.views import BookingViewSet

router = routers.DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')

urlpatterns = [

    path('', include(router.urls)),
    #gets all user profiles and create a new profile
   # retrieves profile details of the currently logged in user
]