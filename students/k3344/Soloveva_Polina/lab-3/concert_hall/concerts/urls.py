from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),

    path('concerts/', views.concert_list, name='concert-list'),
    path('concerts/', views.create_concert, name='create_concert'),
    path('concerts/<int:pk>/', views.concert_detail, name='concert-detail'),
    path('concerts/<int:pk>/', views.update_concert, name='update_concert'),
    path('concerts/<int:pk>/delete/', views.delete_concert, name='delete_concert'),

    path('concerts/equipment/', views.add_equipment_to_concert, name='add_equipment_to_concert'),
    path('concerts/<int:concert_id>/equipment/', views.get_equipment_for_concert, name='get_equipment_for_concert'),
    path('concerts/equipment/<int:pk>/remove/', views.remove_equipment_from_concert,
         name='remove_equipment_from_concert'),
    path('concerts/equipment/<int:pk>/update/', views.update_equipment_for_concert,
         name='update_equipment_for_concert'),

    path('tickets/', views.ticket_list_create, name='ticket-list-create'),
    path('tickets/<int:pk>/', views.ticket_detail, name='ticket-detail'),

    path('orders/', views.order_list_create, name='order-list-create'),
    path('orders/<int:pk>/', views.get_order, name='get_order'),
    path('orders/<int:pk>/confirm/', views.confirm_order, name='confirm-order'),

    path("organizer/assign/<int:pk>/", views.assign_concert, name="assign_concert"),
    path("organizer/concerts/", views.get_organizer_concerts, name="organizer-concerts"),
]