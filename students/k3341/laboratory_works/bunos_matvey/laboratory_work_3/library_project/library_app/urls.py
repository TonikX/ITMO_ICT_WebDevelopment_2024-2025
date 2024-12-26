from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, AuthorViewSet, ReaderViewSet,
    ReadingRoomViewSet
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'readers', ReaderViewSet)
router.register(r'reading-rooms', ReadingRoomViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
