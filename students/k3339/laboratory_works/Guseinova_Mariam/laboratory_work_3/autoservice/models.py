from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Client(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="cars")
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class Worker(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.service_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    ]

    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="orders")
    employee = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, related_name="orders")
    order_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderInfo(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="details")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail {self.order_detail_id} for Order {self.order.order_id}"

class PayProcess(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"

class Qualification(models.Model):
    qualification_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="qualifications")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="qualifications")

    def __str__(self):
        return f"{self.employee.name} - {self.service.service_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
