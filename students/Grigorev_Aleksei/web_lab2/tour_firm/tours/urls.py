from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:tour_id>/reserve/', views.reserve_tour, name='reserve_tour'),
    path('tour/<int:tour_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('register/', views.register, name='register'),
    path('tour/<int:tour_id>/add_review/', views.add_review, name='add_review')# РегистрацияВход
]
