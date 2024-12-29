from django.urls import path, include
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    NewspaperList, NewspaperDetail,
    PrintShopList, PrintShopDetail,
    PrintRunList, PrintRunDetail,
    DeliveryList, DeliveryDetail
)

urlpatterns = [
    # Newspaper
    path('newspapers/', NewspaperList.as_view(), name='newspaper-list'),
    path('newspapers/<int:pk>/', NewspaperDetail.as_view(), name='newspaper-detail'),

    # PrintShop
    path('printshops/', PrintShopList.as_view(), name='printshop-list'),
    path('printshops/<int:pk>/', PrintShopDetail.as_view(), name='printshop-detail'),

    # PrintRun
    path('printruns/', PrintRunList.as_view(), name='printrun-list'),
    path('printruns/<int:pk>/', PrintRunDetail.as_view(), name='printrun-detail'),

    # Delivery
    path('deliveries/', DeliveryList.as_view(), name='delivery-list'),
    path('deliveries/<int:pk>/', DeliveryDetail.as_view(), name='delivery-detail'),

    path('auth/', include('djoser.urls')),  # Регистрация и авторизация
    path('auth/token/', obtain_auth_token),  # Получение токена
    path('auth/users/me/', include('djoser.urls.authtoken')),  # Информация о текущем пользователе
]
