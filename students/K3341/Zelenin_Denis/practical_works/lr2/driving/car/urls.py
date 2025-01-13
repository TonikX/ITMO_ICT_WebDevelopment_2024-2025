from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.car_detail),
    path('owner/list/', views.owners_list),
    path('car/list/', views.CarListView.as_view(), name='car_list'),
    path('car/<int:pk>/', views.CarDetail.as_view(), name = 'car_detail'),
    path('owner/create/', views.OwnerCreateView),
    path('car/<int:pk>/update/', views.PublisherUpdateView.as_view(), name='update_car'),
    path('car/<int:pk>/delete', views.CarDelete.as_view(), name='delete_car')
]
