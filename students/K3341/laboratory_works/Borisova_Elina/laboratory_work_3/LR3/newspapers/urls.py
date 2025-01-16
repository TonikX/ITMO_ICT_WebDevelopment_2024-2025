from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EditorViewSet, NewspaperViewSet, PrintShopViewSet, PostOfficeViewSet, PrintRunViewSet, DeliveryViewSet

router = DefaultRouter()
router.register(r'editors', EditorViewSet)
router.register(r'newspapers', NewspaperViewSet)
router.register(r'printshops', PrintShopViewSet)
router.register(r'postoffices', PostOfficeViewSet)
router.register(r'printruns', PrintRunViewSet)
router.register(r'deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]