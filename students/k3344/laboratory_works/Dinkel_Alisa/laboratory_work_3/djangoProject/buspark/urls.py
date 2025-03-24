from django.urls import path
from .views import (
    BusCategoryListCreateView, BusCategoryRetrieveUpdateDestroyView,
    BusListCreateView, BusRetrieveUpdateDestroyView,
    DriverListCreateView, DriverRetrieveUpdateDestroyView,
    RouteListCreateView, RouteRetrieveUpdateDestroyView,
    ShiftListCreateView, ShiftRetrieveUpdateDestroyView,
    DriversOnRouteView, TotalRouteDistanceView, InactiveBusesView,
    InactiveDriversView, RouteScheduleView, DriverCategoryCountView, ReportView
)

urlpatterns = [
    # Типы автобусов
    # 1 - получить список всех объектов и создать новый объект
    # 2 - # получить конкретный объект, обновить его или удалить
    path('bus-categories/', BusCategoryListCreateView.as_view(), name='bus-category-list'),
    path('bus-categories/<int:pk>/', BusCategoryRetrieveUpdateDestroyView.as_view(), name='bus-category-detail'),

    # Автобусы
    path('buses/', BusListCreateView.as_view(), name='bus-list'),
    path('buses/<int:pk>/', BusRetrieveUpdateDestroyView.as_view(), name='bus-detail'),

    # Водители
    path('drivers/', DriverListCreateView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDestroyView.as_view(), name='driver-detail'),

    # Маршруты
    path('routes/', RouteListCreateView.as_view(), name='route-list'),
    path('routes/<int:pk>/', RouteRetrieveUpdateDestroyView.as_view(), name='route-detail'),

    # Смены
    path('shifts/', ShiftListCreateView.as_view(), name='shift-list'),
    path('shifts/<int:pk>/', ShiftRetrieveUpdateDestroyView.as_view(), name='shift-detail'),

    # Водители на маршруте
    path('routes/<int:route_id>/drivers/', DriversOnRouteView.as_view(), name='drivers-on-route'),

    # Общая продолжительность маршрутов
    path('routes/total-duration/', TotalRouteDistanceView.as_view(), name='total-route-duration'),

    # Автобусы, не вышедшие на линию
    path('buses/inactive/<str:date>/', InactiveBusesView.as_view(), name='inactive-buses'),

    # Водители, не вышедшие на линию
    path('drivers/inactive/<str:date>/', InactiveDriversView.as_view(), name='inactive-drivers'),

    # Время начала и окончания движения автобусов
    path('routes/schedule/', RouteScheduleView.as_view(), name='route-schedule'),

    # Количество водителей по категориям
    path('drivers/category-count/', DriverCategoryCountView.as_view(), name='driver-category-count'),

    # Отчет
    path('reports/park-status/', ReportView.as_view(), name='park_status_report'),
]
