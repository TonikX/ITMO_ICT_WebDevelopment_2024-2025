from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("signup/", views.signup_view, name="signup"),
    path("", views.HotelListView.as_view(), name="hotel_list"),
    path("hotel/<int:pk>/", views.HotelDetailView.as_view(), name="hotel_detail"),
    path("room/<int:room_id>/reserve/", views.reserve_room, name="reserve_room"),
    path("reservations/", views.reservation_list, name="reservation_list"),
    path("reservation/<int:reservation_id>/edit/", views.edit_reservation, name="edit_reservation"),
    path("reservation/<int:reservation_id>/delete/", views.delete_reservation, name="delete_reservation"),
    path("room/<int:room_id>/review/", views.add_review, name="add_review"),
    path("recent-guests/", views.recent_guests, name="recent_guests"),
]
