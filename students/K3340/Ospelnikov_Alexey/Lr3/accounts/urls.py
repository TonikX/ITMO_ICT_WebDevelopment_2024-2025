from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from . import views
from .views import UserProfileListCreateView, UserProfileDetailView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users_register', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('get_guests/', views.get_guests),
    path('get_guests_on_neighbour/', views.get_guests_on_neighbour),

    #gets all user profiles and create a new profile
    path("all-profiles",UserProfileListCreateView.as_view(),name="all-profiles"),
   # retrieves profile details of the currently logged in user
    path("profile/<int:pk>", UserProfileDetailView.as_view(), name="profile"),
]