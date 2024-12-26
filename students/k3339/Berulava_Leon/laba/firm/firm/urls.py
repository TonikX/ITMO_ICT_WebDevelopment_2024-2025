"""
URL configuration for firm project.

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
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tour.views import Index, addTour, tour_detail, basket_add, basket_view, basket_remove, confirm_booking, booking_views

urlpatterns = [
    path("admin/", admin.site.urls), 
    path('', Index, name="Index"),
    path('page/<int:page>', Index, name='paginator'),
    path("users/", include('users.urls', namespace='users')),
    path('addtour/', addTour, name="addTour"),
    path('tour/<int:tour_id>/', tour_detail, name='tour_detail'),
    path('baskets/add/<int:tour_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('basket/', basket_view, name='basket'),
    path('basket/confirm/', confirm_booking, name='confirm_booking'),
    path('bookings/', booking_views, name='booking_views'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
