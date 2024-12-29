from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import sold_tours_by_country

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='log_in.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('review/<int:tour_id>/', views.add_review, name='add_review'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('add_review/<int:tour_id>/', views.add_review, name='add_review'),
    path('sold_tours/', views.sold_tours_by_country, name='sold_tours_by_country')

]
