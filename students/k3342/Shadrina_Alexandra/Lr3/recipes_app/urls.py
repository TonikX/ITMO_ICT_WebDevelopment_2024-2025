from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RecipeViewSet, TagViewSet, RecipeTagViewSet,
    CommentViewSet, SavedRecipeViewSet, SubscriptionViewSet, RatingViewSet
)

app_name = "recipes_app"

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipe-tags', RecipeTagViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'saved-recipes', SavedRecipeViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
