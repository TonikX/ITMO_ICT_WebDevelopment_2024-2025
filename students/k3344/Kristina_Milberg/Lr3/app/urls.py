from django.contrib import admin
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index.as_view(), name='index'),

    # Вместо админ панели
    path('manage/', ManageStateView.as_view(), name='manage'),

    path('manage/agency/', AgencyList.as_view(), name='manage-agency'),
    path('manage/agency/<int:pk>/', AgencyDetail.as_view(), name='manage-agency-detail'),
    path('manage/agency/<int:pk>/add_broker_company',
         CreateBrokerCompany.as_view(),
         name='manage-agency-add-broker-company'),

    # Создать брокеров
    path('manage/broker_company/<int:pk>/', BrokerCompanyDetails.as_view()),
    path('manage/broker_company/<int:pk>/add_broker/', AddBroker.as_view()),

    # Создать продукты для покупки
    path('manage/manufacturer/', ManufacturerList.as_view()),
    path('manage/manufacturer/<int:pk>/', ManufacturerDetail.as_view()),
    path('manage/manufacturer/<int:pk>/add_product/', CreateProduct.as_view()),

    # Списки продуктов
    path('product/', ProductViewSet.as_view({'get': 'list', })),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('product/<int:pk>/order/', OrderProduct.as_view()),

    # Панель брокера
    path('broker/', BrokerList.as_view()),
    path('broker/<int:pk>/', OrderDetail.as_view()),
    path('broker/<int:pk>/approve/', ApproveOrder.as_view()),
    path('broker/statistics/', BrokerStatistics.as_view()),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path("admin/", admin.site.urls),
]
