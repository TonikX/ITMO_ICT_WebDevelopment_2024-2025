from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import (
    ClientViewSet, UserClientInfo, ServiceViewSet, PriceListViewSet, PositionViewSet, EmployeeViewSet,
    PositionEmployeeViewSet, OrderViewSet, PaymentOrderViewSet, CompletedOrdersListView,
    PaymentOrdersByPeriodView, ServiceListView, OrdersByClientView, EmployeeOrdersCountView, QuarterlyReportView,
    RegisterView
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
# --- Настройка маршрутов API ---
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
    # Основные API-роуты
    path('api/', include(router.urls)),
    path('api/client-info/', UserClientInfo.as_view(), name='user-client-info'),
    path("api/auth/users/", RegisterView.as_view(), name="register"),


    # Отдельные вьюхи
    path('api/completed-orders/', CompletedOrdersListView.as_view(), name='completed-orders'),
    path('api/payment-orders-by-period/', PaymentOrdersByPeriodView.as_view(), name='payment-orders-by-period'),
    path('api/service-list/', ServiceListView.as_view(), name='service-list'),
    path('api/orders-by-client/', OrdersByClientView.as_view(), name='orders-by-client'),
    path('api/employee-orders-count/', EmployeeOrdersCountView.as_view(), name='employee-orders-count'),
    path('api/quarterly-report/', QuarterlyReportView.as_view(), name='quarterly-report'),

    # --- Swagger UI ---
    path('api/docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/docs/swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
