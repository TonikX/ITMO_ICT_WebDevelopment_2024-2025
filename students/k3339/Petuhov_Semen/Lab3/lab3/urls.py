"""
URL configuration for lab3 project.

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
from .views import (ClientListView, FlightListView, ScheduleListView, CurrentUserView,ClientCreateView, TicketCreateView, FlightCreateView,CrewCreateView,
                    AircraftCreateView, ScheduleCreateView, AirportCreateView, TransitStopCreateView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', ClientListView.as_view(), name='client-list'),
    path('api/flights/', FlightListView.as_view(), name='flight-list'),
    path('api/schedules/', ScheduleListView.as_view(), name='schedule-list'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('api/clients/create/', ClientCreateView.as_view(), name='client-create'),
    path('api/tickets/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('api/flights/create/', FlightCreateView.as_view(), name='flight-create'),
    path('api/crews/create/', CrewCreateView.as_view(), name='crew-create'),
    path('api/aircrafts/create/', AircraftCreateView.as_view(), name='aircraft-create'),
    path('api/schedules/create/', ScheduleCreateView.as_view(), name='schedule-create'),
    path('api/airports/create/', AirportCreateView.as_view(), name='airport-create'),
    path('api/transit-stops/create/', TransitStopCreateView.as_view(), name='transitstop-create'),
]
