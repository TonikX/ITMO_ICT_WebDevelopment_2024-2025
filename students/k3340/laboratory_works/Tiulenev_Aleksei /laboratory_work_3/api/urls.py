from django.urls import include, path
from rest_framework import routers
from .views import (
    EmployeeViewSet, AuthorViewSet, BookViewSet, BookAuthorViewSet,
    EditionViewSet, ContractViewSet, EditionEditorViewSet,
    CustomerViewSet, OrderViewSet, OrderItemViewSet
)

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-authors', BookAuthorViewSet)
router.register(r'editions', EditionViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'edition-editors', EditionEditorViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]