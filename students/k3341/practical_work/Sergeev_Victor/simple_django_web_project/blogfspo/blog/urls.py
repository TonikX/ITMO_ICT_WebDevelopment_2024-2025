from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.detail_owner),
    path('owner/list/', views.detail_owner_list),
    path('time/', views.example_view),
    path('car/list/', views.CarList.as_view()),
    path('car/<int:pk>/', views.CarRetrieveView.as_view()),
    path('car/crud/', views.CarListCRUD.as_view()),
    path('owner/create', views.create_owner),
    path('car/<int:pk>/update', views.CarUpdateView.as_view()),
    path('car/create/', views.CarCreateView.as_view()),
    path('car/<int:pk>/delete', views.CarDeleteView.as_view())
]
