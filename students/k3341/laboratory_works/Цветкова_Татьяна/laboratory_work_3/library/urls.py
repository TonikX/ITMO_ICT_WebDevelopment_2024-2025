from rest_framework.routers import DefaultRouter
from .views import (
    ReadingRoomViewSet,
    ReaderViewSet,
    BookViewSet,
    BorrowingViewSet
)

router = DefaultRouter()
router.register('rooms', ReadingRoomViewSet)
router.register('readers', ReaderViewSet)
router.register('books', BookViewSet)
router.register('borrowings', BorrowingViewSet)

urlpatterns = router.urls