from django.urls import path
from . import views

urlpatterns = [
    path('сar_owner/<int:car_owner_id>/', views.get_сar_owner_details),
    path('time/', views.example_view),
    path('сar_owners/', views.get_сar_owners),
    # path('cars/', views.CarsList.as_view()),
    path('car/<int:pk>/', views.CarRetrieveView.as_view()),
    path('cars/', views.CarListView.as_view()),
    path('сar_owner/create/', views.create_сar_owner),
    path('car/<int:pk>/update/', views.CarUpdateView.as_view()),
    path('car/create/', views.CarCreateView.as_view(success_url="/cars/")),
    path('car/<int:pk>/delete/', views.CarDeleteView.as_view()),
]

