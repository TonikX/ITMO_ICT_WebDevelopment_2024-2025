from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    AgencyViewSet, BrokerViewSet, ProducerViewSet,
    ProductViewSet, BatchViewSet, BatchProductViewSet,
    ClientViewSet, ClientPurchaseViewSet, TransactionViewSet
)

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'brokers', BrokerViewSet, basename='broker')
router.register(r'producers', ProducerViewSet, basename='producer')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'batch-products', BatchProductViewSet, basename='batch-product')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'client-purchases', ClientPurchaseViewSet, basename='client-purchase')
router.register(r'transactions', TransactionViewSet, basename='transaction')

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API documentation",
        contact=openapi.Contact(email="contact@yourapi.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[path('api/', include(router.urls))],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
