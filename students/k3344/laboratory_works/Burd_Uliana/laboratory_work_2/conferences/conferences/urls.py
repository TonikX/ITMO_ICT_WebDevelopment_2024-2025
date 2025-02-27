from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('confapp.urls')),
    path('', lambda request: redirect('login/'), name='index')
]
