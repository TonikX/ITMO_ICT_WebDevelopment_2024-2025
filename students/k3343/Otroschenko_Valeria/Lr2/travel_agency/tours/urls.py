from django.contrib import admin
from django.urls import path, include
from . import views as tour_views

app_name = 'tours'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', tour_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', tour_views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', tour_views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/reserve/', tour_views.reserve_tour, name='reserve_tour'),
    path('my_reservations/', tour_views.my_reservations, name='my_reservations'),
    path('reservation/delete/<int:reservation_id>/', tour_views.delete_reservation, name='delete_reservation'),
    path('tour/<int:tour_id>/review/', tour_views.add_review, name='add_review'),
    path('sold_tours/', tour_views.sold_tours_by_country, name='sold_tours_by_country'),
    path('reservation/delete/<int:reservation_id>/', tour_views.delete_reservation, name='delete_reservation'),
]