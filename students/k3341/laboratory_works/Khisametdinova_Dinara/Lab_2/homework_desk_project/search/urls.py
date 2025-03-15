from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.AdminSearchView.as_view(), name='index'),
]
