from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WarriorViewSet

router = DefaultRouter()
router.register(r'warriors', WarriorViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
