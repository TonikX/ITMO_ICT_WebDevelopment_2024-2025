from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class Service(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)
    materials = models.TextField()

class PriceList(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_price = models.DateTimeField()
    end_price = models.DateTimeField()

class Position(models.Model):
    position_title = models.CharField(max_length=255)

class Employee(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class PositionEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    completion_date = models.DateTimeField()
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

class PaymentOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_order_date = models.DateTimeField()
    payment_date = models.DateTimeField()
    payment_status = models.CharField(max_length=50)

class ServiceOrder(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)