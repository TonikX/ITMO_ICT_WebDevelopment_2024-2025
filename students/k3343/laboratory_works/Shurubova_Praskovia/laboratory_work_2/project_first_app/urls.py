from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import ReservationCreateView, ReviewCreateView, UserReservationsView, \
    UserRegistrationView, TourListView, TourDetailView, HomeView, \
    CustomLogoutView, AdminApproveReservationView, AdminReservationsView, \
    ConfirmedToursByCountryView, UserConfirmedToursByCountryView, CancelReservationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('tours/', TourListView.as_view(), name='tour_list'),
    path('confirmed-tours-by-country/', ConfirmedToursByCountryView.as_view(), name='confirmed_tours_by_country'),
    path('user-confirmed-tours-by-country/', UserConfirmedToursByCountryView.as_view(), name='user_confirmed_tours_by_country'),
    path('tour/<int:tour_id>/', TourDetailView.as_view(), name='tour_detail'),
    path('tour/<int:tour_id>/reserve_tour/<int:user_id>/', ReservationCreateView.as_view(), name='reserve_tour'),
    path('tour/<int:tour_id>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('user_reservations/', UserReservationsView.as_view(), name='user_reservations'),
    path('admin_reservations/', AdminReservationsView.as_view(), name='admin_reservations'),
    path('admin_reservations/approve/<int:reservation_id>/', AdminApproveReservationView.as_view(), name='approve_reservation'),
    path('reservation/cancel/<int:reservation_id>/', CancelReservationView.as_view(), name='cancel_reservation'),
]
