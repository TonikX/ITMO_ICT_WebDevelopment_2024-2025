from django.urls import path

from . import views
from .apps import ReviewsConfig

app_name = ReviewsConfig.name

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='index'),
    path('add/<int:pk>/', views.AddReviewView.as_view(), name='add'),
]