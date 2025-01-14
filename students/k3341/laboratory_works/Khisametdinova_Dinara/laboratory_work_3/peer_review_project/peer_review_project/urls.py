"""
URL configuration for peer_review_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v2',
      description="Peer review app API docs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="hardbeat34@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_info = openapi.Info(
    title="Peer Review API",
    default_version='v1',
    description="Описание API для системы Peer Review",
    terms_of_service="https://www.example.com/terms/",
    contact=openapi.Contact(email="support@example.com"),
    license=openapi.License(name="MIT License"),
)   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('peer/', include('peer_review_app.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
