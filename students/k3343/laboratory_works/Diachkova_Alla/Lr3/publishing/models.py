from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.CharField(max_length=200)
    position = models.CharField(max_length=50)
    is_editor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)


class Contract(models.Model):
    creation_date = models.DateField()
    signature_date = models.DateField()
    manager = models.ForeignKey(Employee, on_delete=models.PROTECT)
    is_active = models.CharField(max_length=10)
    pay_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Author(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.CharField(max_length=200)


class Book(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)
    page_count = models.IntegerField()
    has_illustrations = models.BooleanField(default=False)
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT)
    editors = models.ManyToManyField(Employee, through='EditingJob')
    authors = models.ManyToManyField(Author, through='BookAuthor')
    release_date = models.DateField()


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    author_order = models.IntegerField()
    royalty_percentage = models.DecimalField(max_digits=5, decimal_places=2)


class EditingJob(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    editor = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assignment_date = models.DateField()
    is_lead_editor = models.BooleanField(default=False)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    contacts = models.CharField(max_length=200)
    delivery_address = models.CharField(max_length=200)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateField()
    delivery_status = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2)
