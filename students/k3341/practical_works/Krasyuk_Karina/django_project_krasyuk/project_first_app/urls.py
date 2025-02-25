from django.urls import path

from project_first_app import views
from project_first_app.views import CarsList, CarRetrieveView, CarUpdateView, create_owner, CarCreateView, \
    CarDeleteView

urlpatterns = [
    path('owners/<int:owner_id>/', views.owner),
    path('owners/', views.owners),
    path('cars/', CarsList.as_view()),
    path('cars/<int:pk>/', CarRetrieveView.as_view()),
    path('cars/<int:pk>/update/', CarUpdateView.as_view()),
    path('cars/<int:pk>/delete/', CarDeleteView.as_view()),
    path('cars/create/', CarCreateView.as_view()),
    path('owners/create', create_owner)

]
