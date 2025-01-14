from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('hotels/', views.get_all_hotels, name='all_hotels'),
    path('hotels/<int:hotel_id>/', views.get_hotel_info, name='hotel_info'),
    path('user_reservations/', views.user_get_all_reservations, name='user_reservations'),
    path('admin_reservations/', views.admin_get_all_reservations, name='admin_reservations'),
    path('update_reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('create_reservation/<int:room_id>/', views.create_reservation, name='create_reservation'),
    path('all_reviews/<int:room_id>/', views.get_all_reviews, name='all_reviews'),
    path('create_review/<int:reservation_id>/', views.create_review, name='create_review'),
    path('admin_reservations/confirm/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('admin_reservations/decline/<int:reservation_id>/', views.decline_reservation, name='decline_reservation'),
]

