from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .views import QuarterReportAPIView


router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'guests', GuestViewSet)
router.register(r'stays', StayViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'schedules', CleaningScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/quarter/', QuarterReportAPIView.as_view()),
]
