from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('owner/detail/<int:car_owner_id>', views.detail),
    path('owner/list/', views.owners, name='owners'),
    path('car/list/', views.CarList.as_view()),
    path('car/<int:pk>', views.CarDetail.as_view()),
    path('owner/create/', views.create_owner),
    path('car/<int:pk>/edit', views.CarUpdateView.as_view()),
    path('car/create/', views.CarCreate.as_view()),
    path('car/<int:pk>/delete', views.CarDeleteView.as_view())
]
