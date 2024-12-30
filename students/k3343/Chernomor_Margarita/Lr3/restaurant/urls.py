from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from restaurant.views import RestaurantListCreateView, RestaurantDetailView, TableListView, ReservationCreateView, \
    RestaurantReviewsListCreateView, MyRestaurantsListView, MyRestaurantReviewsListView, MyRestaurantBookingListView, \
    MyBookingListView

schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant booking api",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    path('restaurants/', RestaurantListCreateView.as_view()),
    path('restaurants/<int:pk>/', RestaurantDetailView.as_view()),
    path('restaurants/<int:pk>/tables/', TableListView.as_view()),

    path('restaurants/<int:pk>/tables/<int:tpk>/', ReservationCreateView.as_view()),

    path('restaurants/<int:pk>/reviews/', RestaurantReviewsListCreateView.as_view()),

    path('my/restaurants/', MyRestaurantsListView.as_view()),
    path('my/restaurants/<int:pk>/', MyRestaurantBookingListView.as_view()),
    path('my/restaurants/<int:pk>/reviews/', MyRestaurantReviewsListView.as_view()),

    path('my/booking/', MyBookingListView.as_view()),




    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("admin/", admin.site.urls),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
