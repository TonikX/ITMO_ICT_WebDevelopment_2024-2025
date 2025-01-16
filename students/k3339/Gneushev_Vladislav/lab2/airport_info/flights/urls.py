from django.urls import path

from . import views

urlpatterns = [
    path('', views.FlightsList.as_view(), name='flights_list'),
    path('<int:flight_id>/', views.flight_details, name='flight_details'),
    path('<int:flight_id>/add_review/', views.add_review, name='add_review'),
    path('<int:flight_id>/reserve/', views.reserve_ticket, name='reserve_ticket'),
    path('ticket/reservation/<int:reservation_id>/confirm/', views.confirm_reservation, name='confirm_reservation'),
    path('ticket/reservation/<int:reservation_id>/delete/', views.delete_ticket_reservation, name='delete_reservation'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket')
]
