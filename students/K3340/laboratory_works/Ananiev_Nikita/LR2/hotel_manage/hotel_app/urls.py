from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main_page'),
    path('hotel/<int:pk>/', views.HotelDetailView.as_view(), name="hotel_details"),
    path('hotel/<int:pk>/room/', views.RoomListView.as_view(), name="room_list"),
    path('hotel/', views.HotelListView.as_view(), name="hotel_list"),
    path('hotel/<int:pk>/room/<int:id>/', views.RoomDetailView.as_view(), name="room_details"),
    path('hotel/<int:pk>/residents/', views.ResidentsListView.as_view(), name="resident_list"),
]
