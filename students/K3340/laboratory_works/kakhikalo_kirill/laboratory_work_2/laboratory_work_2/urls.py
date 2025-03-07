from django.urls import path, include
from django.contrib import admin
from flights import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.FlightListView.as_view(), name='flight_list'),
    path('flight/<int:pk>/', views.FlightDetailView.as_view(), name='flight_detail'),
    path('reservation/create/<int:flight_id>/', views.create_reservation, name='create_reservation'),
    path('reservation/edit/<int:pk>/', views.ReservationUpdateView.as_view(), name='reservation_edit'),
    path('reservation/delete/<int:pk>/', views.ReservationDeleteView.as_view(), name='reservation_delete'),
    path('flight/<int:flight_id>/comment/', views.create_comment, name='create_comment'),
]
