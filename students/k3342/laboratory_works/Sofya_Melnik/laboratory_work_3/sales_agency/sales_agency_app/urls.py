from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import (
    ClientViewSet, ServiceViewSet, PriceListViewSet, PositionViewSet, EmployeeViewSet,
    PositionEmployeeViewSet, OrderViewSet, PaymentOrderViewSet, CompletedOrdersListView,
    PaymentOrdersByPeriodView, ServiceListView, OrdersByClientView, EmployeeOrdersCountView, QuarterlyReportView
)

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Луч API",
        default_version='v1',
        description="Документация API для рекламного агентства 'Луч'",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Создание маршрутов API
router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'price-list', PriceListViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'employees', EmployeeViewSet)
router.register(r'position-employees', PositionEmployeeViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'payment-orders', PaymentOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('completed-orders/', CompletedOrdersListView.as_view(), name='completed-orders'),
    path('payment-orders-by-period/', PaymentOrdersByPeriodView.as_view(), name='payment-orders-by-period'),
    path('service-list/', ServiceListView.as_view(), name='service-list'),
    path('orders-by-client/', OrdersByClientView.as_view(), name='orders-by-client'),
    path('employee-orders-count/', EmployeeOrdersCountView.as_view(), name='employee-orders-count'),
    path('quarterly-report/', QuarterlyReportView.as_view(), name='quarterly-report'),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>.json|.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]