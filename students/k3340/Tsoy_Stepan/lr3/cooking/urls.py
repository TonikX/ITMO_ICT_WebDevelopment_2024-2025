from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('recipes/', MealListCreateAPIView.as_view(), name='meal-list-create'),
    path('recipes/<int:pk>/', MealDetailAPIView.as_view(), name='meal-detail'),
    path('recipes/<int:pk>/steps/', StepListCreateAPIView.as_view(), name='meal-step-list'),
    path('recipes/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name='meal-comments-list'),
    path('recipes/<int:pk>/like/', LikeView.as_view(), name='meal-like'),

    path('account/', AccountView.as_view(), name='account'),
    path('account/posts/', MyRecipesView.as_view(), name='account-recipes'),
    path('account/comments/', MyCommentsView.as_view(), name='account-comments'),
    path('account/likes/', MyLikesView.as_view(), name='account-comments'),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("admin/", admin.site.urls),
    ]