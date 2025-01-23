from django.urls import path
from . import views
from .views import CarListView, CarDetailView, create_owner_view, CarCreateView, CarUpdateView, CarDeleteView

urlpatterns = [
    path('car_owner/<int:car_owner_id>/', views.car_owner_detail),
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/create/', create_owner_view, name='owner_create'),
    # path('owner_list/', views.owner_list),

    path('cars/', CarListView.as_view(), name='car_list'),
    path('car_detail/<int:pk>/', CarDetailView.as_view()),
    # path('create_owner/', create_owner_view),
    path('car_update/<int:pk>/', CarUpdateView.as_view()),
    path('car_delete/<int:pk>/', CarDeleteView.as_view()),
    path('car_form/', CarCreateView.as_view()),
]
