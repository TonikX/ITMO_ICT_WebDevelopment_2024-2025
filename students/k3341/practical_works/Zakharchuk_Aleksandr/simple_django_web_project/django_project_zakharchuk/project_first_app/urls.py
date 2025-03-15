from django.urls import path

from project_first_app import views

urlpatterns = [
    path("owners/create", views.create_owner),
    path("owners/<int:owner_id>/", views.owner),
    path("owners/", views.owners),
    path("cars/create/", views.CarCreateView.as_view()),
    path("cars/<int:pk>/", views.CarDetailView.as_view()),
    path("cars/", views.CarsListView.as_view()),
    path("cars/<int:pk>/update/", views.CarUpdateView.as_view()),
    path("cars/<int:pk>/delete/", views.CarDeleteView.as_view()),
]
