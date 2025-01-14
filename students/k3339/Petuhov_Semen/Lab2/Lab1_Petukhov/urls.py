from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='tour_list'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('', views.tour_list, name='tour_list'),
    path('tour/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('reserve/<int:tour_id>/', views.reserve_tour, name='reserve_tour'),
    path('my_tours/', views.my_tours, name='my_tours'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('tour/<int:tour_id>/add_comment/', views.add_comment, name='add_comment'),
    path('confirmed_tours_by_country/', views.confirmed_tours_by_country, name='confirmed_tours_by_country'),
]
