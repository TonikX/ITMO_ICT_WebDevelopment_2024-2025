# Ссылки

## Описание

Реализовать ссылки для приложения.

## Стек

- Python
- django
- restFramework
- djoser
- drf_yasg

## Листинг

### urls.py:

```python
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Bus API",
      default_version='v1',
      description="Документация API для системы управления автобусами",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="prokopecsemen@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lr3app.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```
```python
from django.urls import include, path
from rest_framework import routers
from .views import (
    BusTypeViewSet,
    BusViewSet,
    DriverViewSet,
    RouteViewSet,
    WorkShiftViewSet,
    DriversByRouteView,
    RouteStatsViewSet,
)

router = routers.DefaultRouter()
router.register(r'bus-types', BusTypeViewSet)
router.register(r'buses', BusViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'work-shifts', WorkShiftViewSet)
router.register(r'route-stats', RouteStatsViewSet, basename='route-stats')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
urlpatterns += [
    path('drivers/route/<int:route_id>/', DriversByRouteView.as_view(), name='drivers-by-route'),
]
```