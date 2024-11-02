from django.urls import path
from . import views
urlpatterns = [
    path('owners/<int:owner_id>/', views.owner),
    path('owners/', views.owner_list),
    path('owners/create/', views.create_owner_view),
    path('cars/', views.CarList.as_view()),
    path('cars/<int:pk>/', views.CarRetrieveView.as_view()),
    path('cars/<int:pk>/update/', views.CarUpdateView.as_view()),
    path('cars/create/', views.CarCreateView.as_view()),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view()),
]
