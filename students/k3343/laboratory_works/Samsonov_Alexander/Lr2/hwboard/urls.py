from django.contrib import admin
from django.urls import path, include
from .views import index, RootView

urlpatterns = [
    path('', RootView.as_view(), name='root'),
]