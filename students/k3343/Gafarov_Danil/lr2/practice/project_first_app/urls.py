from django.urls import path
from . import views

urlpatterns = [
    path('driver/<int:driver_id>/', views.driver),
    path('alldrivers/', views.alldrivers),
    path('allcars/', views.allcars),
    path('car/<int:pk>/', views.carView.as_view()),
    path('car/<int:pk>/update/', views.updatecarView.as_view()),
    path('car/<int:pk>/delete/', views.deletecarView.as_view()),
    path('createcar/', views.createcar.as_view()),
    path('createdriver/', views.createdriverView)
 ]