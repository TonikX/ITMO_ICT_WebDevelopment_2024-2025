from django.urls import path
from . import views

urlpatterns = [
    path('owner_create', views.create_owner),
    path('owner/<int:car_owner_id>/', views.get_owner),
    path('owners/', views.list_owners),

    path('car/<int:pk>/', views.GetCarView.as_view()),
    path('cars/', views.ListCarsView.as_view()),
    path('car_update/<int:pk>', views.UpdateCarView.as_view()),
    path('car_create/', views.CreateCarView.as_view()),
    path('car_update_form/<int:pk>', views.UpdateCarFormView.as_view()),
    path('car_delete/<int:pk>', views.DeleteCarView.as_view()),
]