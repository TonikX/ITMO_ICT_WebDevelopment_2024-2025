from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, CarViewSet, EmployeeViewSet,
    ServiceViewSet, OrderViewSet, OrderDetailsViewSet,
    PaymentViewSet, QualificationViewSet, ServiceAnalytics, OrderStatusAnalytics, RegisterView, LoginView, UserInfoView, AverageServiceCostView, TopCustomersView
)

router = DefaultRouter()
router.register(r'clients', CustomerViewSet)
router.register(r'cars', CarViewSet)
router.register(r'workers', EmployeeViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-details', OrderDetailsViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'qualifications', QualificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/service-type/', ServiceAnalytics.as_view(), name='service-type'),
    path('analytics/order-status/', OrderStatusAnalytics.as_view(), name='order-status'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('analytics/average_service_cost/', AverageServiceCostView.as_view(), name='average_service_cost'),
    path('analytics/top_customers/', TopCustomersView.as_view(), name='top_customers'),
]
