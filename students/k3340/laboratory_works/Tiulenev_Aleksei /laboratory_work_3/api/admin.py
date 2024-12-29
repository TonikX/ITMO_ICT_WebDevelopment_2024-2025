from django.contrib import admin
from .models import (
    Employee, Author, Book, BookAuthor, Edition, Contract,
    EditionEditor, Customer, Order, OrderItem
)

admin.site.register(Employee)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookAuthor)
admin.site.register(Edition)
admin.site.register(Contract)
admin.site.register(EditionEditor)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)