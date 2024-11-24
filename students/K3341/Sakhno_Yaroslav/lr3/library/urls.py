from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('library/', include('library_app.urls')),
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),
]
