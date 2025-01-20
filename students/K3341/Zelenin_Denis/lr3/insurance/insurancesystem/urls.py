from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication
from rest_framework.routers import DefaultRouter

from .views import (InsuranceAgentViewSet, OrganizationViewSet, CollectiveContractViewSet,
                    InsuranceCaseViewSet, EmploymentContractViewSet, EmployeeCaseViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v2',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="progavanlav@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),  # Добавлено для поддержки аутентификации по токену
)

router = DefaultRouter()
router.register(r'agents', InsuranceAgentViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'collective-contracts', CollectiveContractViewSet)
router.register(r'insurance-cases', InsuranceCaseViewSet)
router.register(r'employment-contracts', EmploymentContractViewSet)
router.register(r'employee', EmployeeCaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]