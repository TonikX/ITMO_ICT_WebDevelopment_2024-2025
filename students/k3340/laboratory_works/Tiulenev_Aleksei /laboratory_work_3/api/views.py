from rest_framework import viewsets
from .models import (
    Employee, Author, Book, BookAuthor, Edition, Contract,
    EditionEditor, Customer, Order, OrderItem
)
from .serializers import (
    EmployeeSerializer, AuthorSerializer, BookSerializer, BookAuthorSerializer,
    EditionSerializer, ContractSerializer, EditionEditorSerializer,
    CustomerSerializer, OrderSerializer, OrderItemSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookAuthorViewSet(viewsets.ModelViewSet):
    queryset = BookAuthor.objects.all()
    serializer_class = BookAuthorSerializer

class EditionViewSet(viewsets.ModelViewSet):
    queryset = Edition.objects.all()
    serializer_class = EditionSerializer

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class EditionEditorViewSet(viewsets.ModelViewSet):
    queryset = EditionEditor.objects.all()
    serializer_class = EditionEditorSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer