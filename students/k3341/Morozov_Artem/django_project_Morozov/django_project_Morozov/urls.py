"""
URL configuration for django_project_Morozov project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from project_first_app import views
from project_first_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('owner/<int:owner_id>/', views.owner_detail, name='owner_detail'),
    path('example_list/', list_view),
    path('сvb_example/', ExampleList.as_view()),
    path('publisher/<int:pk>/', PublisherRetrieveView.as_view()),
    path('book/list/', BookListView.as_view()),
    path('owner_list/', list_view_owners),
    path('car_list/', CarList.as_view()),
    path('car/<int:pk>/', views.CarRetrieveView.as_view()),
    path('example_create/', create_view),
    path('publisher/<int:pk>/update/', PublisherUpdateView.as_view()),
    path('cvb_example_create/', ExampleCreate.as_view(success_url="/сvb_example/")),
    path('publisher/create/', PublisherCreateView.as_view()),
    path('publisher/<int:pk>/delete/', PublisherDeleteView.as_view()),
    path('owner_create/', owner_create),
    path('car/create/', CarCreateView.as_view(), name='car_create'),
    path('car/<int:pk>/update/', CarUpdateView.as_view(), name='car_update'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),
    path('car/list/', CarList.as_view(), name='car_list'),
]
