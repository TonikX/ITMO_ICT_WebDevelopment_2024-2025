from django.urls import path
from . import views

urlpatterns = [
    path('', views.starting_page, name='starting_page'),
    path('register/', views.register, name='register'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('reserve/create/', views.room_reserve, name='room_reserve'),
    path('reserve/', views.reserve_list, name='reserve_list'),
    path('reserve/<int:pk>/delete/', views.ReserveDeleteView.as_view(), name='delete_reserve'),
    path('review/<int:hotel_id>/', views.write_review, name='write_review'),
    path('lastmonth/', views.last_month_guests, name='last_month_guests'),
]
