from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)

router.register(r'room-types', views.RoomTypeViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'room-prices', views.RoomPriceViewSet)

router.register(r'cleaning-schedules', views.CleaningScheduleViewSet)

router.register(r'bookings', views.BookingViewSet)

router.register(r'job-titles', views.JobTitleViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'employment-contracts', views.EmploymentContractViewSet)




urlpatterns = [
    path('', include(router.urls)),
]