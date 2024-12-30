from django.urls import path
from . import views
from .views import TourUpdateView

urlpatterns = [
    path('', views.home, name='home'),
    path('sold_tours/', views.sold_tours_by_country, name='sold_tours_by_country'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('tours/', views.tour_firm_list, name='tour_firm_list'),
    path('tours/<int:tour_id>/', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/book/', views.book_tour, name='book_tour'),
    path('my_reservations/', views.my_reservations, name='my_reservations'),
    path('tour/<int:tour_id>/add_review/', views.add_review, name='add_review'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('tour/<int:tour_id>/reviews/', views.tour_reviews, name='tour_reviews'),
    path('tour/<int:tour_id>/update/', TourUpdateView.as_view(), name='tour_update'),
    path('reservation/<int:reservation_id>/delete/', views.cancel_reservation, name='reservation_delete'),
    path('all_reservations/', views.all_reservations, name='all_reservations'),
    path('reservation_delete/<int:reservation_id>/', views.reservation_delete, name='reservation_delete'),
    path('tour/add/', views.add_agency, name='add_agency'),
    path('tour/delete/<int:tour_id>/', views.delete_tour, name='delete_tour'),
    path('add_tour/', views.add_tour, name='add_new_tour'),
]
