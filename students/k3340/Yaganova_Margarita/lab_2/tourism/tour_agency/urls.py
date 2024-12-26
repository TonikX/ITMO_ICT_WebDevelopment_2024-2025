from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tour_list, name='tour_list'),
    path('tours/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.TouristLoginView.as_view(), name='login'),
    path('account/', views.account, name='account'),
    path('booking/<int:tour_id>/', views.booking, name='booking'),
    path('edit_tour/<int:booking_id>/', views.edit_tour, name='edit_tour'),
    path('review/<int:tour_id>/<int:booking_id>/', views.review, name='review'),
    path('delete_booking/<int:booking_id>/', views.delete_booking,
         name='delete_booking'),
    path('logout/', views.TouristLogoutView.as_view(), name='logout'),
    path('tour_table/', views.tour_table, name='tour_table')
]
