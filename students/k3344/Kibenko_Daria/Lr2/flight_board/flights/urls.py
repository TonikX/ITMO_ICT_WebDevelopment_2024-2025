from django.urls import path
from . import views

urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reserve/<int:flight_id>/', views.reserve_seat, name='reserve_seat'),
    path('reviews/<int:flight_id>/', views.flight_reviews, name='flight_reviews'),
    path('add_review/<int:flight_id>/', views.add_review, name='add_review'),
]
