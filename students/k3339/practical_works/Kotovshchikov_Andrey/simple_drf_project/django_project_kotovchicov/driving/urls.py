from driving import views
from django.urls import path

urlpatterns = [
    path(
        "owner/create",
        views.car_owner_create_view,
        name="owner-create",
    ),
    path(
        "owner/<int:owner_pk>/",
        views.car_owner_view,
        name="owner",
    ),
    path(
        "owner/list/",
        views.car_owner_list_view,
        name="owner-list",
    ),
    path(
        "car/list/",
        views.CarListView.as_view(),
        name="car-list",
    ),
    path(
        "car/<int:car_pk>/",
        views.CarDetailView.as_view(),
        name="car",
    ),
    path(
        "car/create/",
        views.CarCreateView.as_view(),
        name="car-create",
    ),
    path(
        "car/<int:car_pk>/update/",
        views.CarUpdateView.as_view(),
        name="car-update",
    ),
    path(
        "car/<int:car_pk>/delete/",
        views.CarDeleteView.as_view(),
        name="car-delete",
    ),
]
