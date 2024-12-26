from django.urls import path
from project_first_app.views import *

urlpatterns = [
    path('get_owner/<int:owner_id>', get_owner),
    path('get_owners', get_owners),
    path('create_owner', create_owner),
    path('get_car/<int:pk>', GetCarView.as_view()),
    path('get_cars', GetCarsView.as_view()),
    path('create_car', CreateCarView.as_view()),
    path('update_car/<int:pk>', UpdateCarView.as_view()),
    path('delete_car/<int:pk>', DeleteCarView.as_view()),
]
