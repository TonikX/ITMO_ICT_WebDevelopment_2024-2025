"""
URL configuration for Lr3 project.

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
from django.urls import path, include

from .views import RecipeDetailView, RecipeListCreateView, CommentListCreateView, CommentDetailView, CuratedListView, \
    CuratedListDetailedView

urlpatterns = [
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),

    path('comments/', CommentListCreateView.as_view(), name='comment-list-retrieve/create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('lists/', CuratedListView.as_view(), name='all_lists'),
    path('lists/<int:pk>', CuratedListDetailedView.as_view(), name='lists-detail'),
    path("admin/", admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
