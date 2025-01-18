from django.urls import path
from . import views

urlpatterns = [
    path('owner/<int:owner_id>/', views.owner_view),
    path('owner/create/', views.add_owner),
    path('owner/', views.all_owners),
    path('car_list/<int:pk>', views.CarDetailView.as_view()),
    path('car_list/', views.CarListView.as_view()),
    path('car_list/create/', views.CarCreateView.as_view()),
    path('car_list/<int:pk>/edit/', views.CarUpdateView.as_view()),
    path('car_list/<int:pk>/delete/', views.CarDeleteView.as_view()),
]
