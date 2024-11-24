from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'library_app'

router = DefaultRouter()
router.register('reader', viewset=ReaderViewSet)
router.register('category', viewset=CategoryViewSet)
router.register('author', viewset=AuthorViewSet)
router.register('reading-room', viewset=ReadingRoomViewSet)
router.register('book', viewset=BookViewSet)
router.register('book-copy', viewset=BookCopyViewSet)
router.register('book-taken', viewset=BookTakeViewSet)

urlpatterns = router.urls