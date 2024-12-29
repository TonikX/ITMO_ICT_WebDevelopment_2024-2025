from django.urls import path 
from . import views

urlpatterns = [
  path('owner/', views.owners),
  path('owner/<int:pk>/', views.owner),
  path('car/', views.CarList.as_view()),
  path('car/<int:pk>/', views.CarDetail.as_view()),
  path('owner/create/', views.owner_create),
  path('car/<int:pk>/update/', views.CarUpdate.as_view()),
  path('car/create/', views.CarCreate.as_view()),
  path('car/<int:pk>/delete/', views.CarDelete.as_view()),
]