from django.urls import path
from .views import *

urlpatterns = [
    # Пользователи
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user-delete'),

    # Газеты
    path('newspapers/create/', NewspaperCreateAPIView.as_view(), name='newspaper-create'),
    path('newspapers/', NewspaperListAPIView.as_view(), name='newspaper-list'),
    path('newspapers/<int:pk>/', NewspaperDetailAPIView.as_view(), name='newspaper-detail'),
    path('newspapers/update/<int:pk>/', NewspaperUpdateAPIView.as_view(), name='newspaper-update'),
    path('newspapers/delete/<int:pk>/', NewspaperDeleteAPIView.as_view(), name='newspaper-delete'),

    # Типографии
    path('printinghouses/create/', PrintingHouseCreateAPIView.as_view(), name='printinghouse-create'),
    path('printinghouses/', PrintingHouseListAPIView.as_view(), name='printinghouse-list'),
    path('printinghouses/<int:pk>/', PrintingHouseDetailAPIView.as_view(), name='printinghouse-detail'),
    path('printinghouses/update/<int:pk>/', PrintingHouseUpdateAPIView.as_view(), name='printinghouse-update'),
    path('printinghouses/delete/<int:pk>/', PrintingHouseDeleteAPIView.as_view(), name='printinghouse-delete'),

    # Почтовые отделения
    path('postoffices/create/', PostOfficeCreateAPIView.as_view(), name='postoffice-create'),
    path('postoffices/', PostOfficeListAPIView.as_view(), name='postoffice-list'),
    path('postoffices/<int:pk>/', PostOfficeDetailAPIView.as_view(), name='postoffice-detail'),
    path('postoffices/update/<int:pk>/', PostOfficeUpdateAPIView.as_view(), name='postoffice-update'),
    path('postoffices/delete/<int:pk>/', PostOfficeDeleteAPIView.as_view(), name='postoffice-delete'),

    # Тиражи
    path('editions/create/', EditionCreateAPIView.as_view(), name='edition-create'),
    path('editions/', EditionListAPIView.as_view(), name='edition-list'),
    path('editions/<int:pk>/', EditionDetailAPIView.as_view(), name='edition-detail'),
    path('editions/update/<int:pk>/', EditionUpdateAPIView.as_view(), name='edition-update'),
    path('editions/delete/<int:pk>/', EditionDeleteAPIView.as_view(), name='edition-delete'),

    # Поставки
    path('distributions/create/', DistributionCreateAPIView.as_view(), name='distribution-create'),
    path('distributions/', DistributionListAPIView.as_view(), name='distribution-list'),
    path('distributions/<int:pk>/', DistributionDetailAPIView.as_view(), name='distribution-detail'),
    path('distributions/update/<int:pk>/', DistributionUpdateAPIView.as_view(), name='distribution-update'),
    path('distributions/delete/<int:pk>/', DistributionDeleteAPIView.as_view(), name='distribution-delete'),

    # Запросы с аналитикой
    path('newspapers/addresses/', NewspaperAddressesAPIView.as_view(), name='newspaper-addresses'),
    path('printinghouses/top-editor/', TopEditorByPrintingHouseAPIView.as_view(), name='top-editor'),
    path('postoffices/expensive-newspapers/', ExpensiveNewspaperOfficesAPIView.as_view(), name='expensive-newspapers'),
    path('distributions/low-quantity/', LowQuantityDistributionsAPIView.as_view(), name='low-quantity-distributions'),
    path('distributions/destination-by-address/', NewspaperDestinationByAddressAPIView.as_view(),
         name='destination-by-address'),

    # Отчет
    path('reports/printinghouses/', PrintingHouseReportAPIView.as_view(), name='printinghouse-report'),
]
