from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=40)
    email = models.EmailField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.full_name


class CarWorkshop(models.Model):
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.city}, {self.address}"


class JobPosition(models.Model):
    name = models.CharField(max_length=20)
    specialisation = models.CharField(max_length=20)
    salary = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=20, blank=True, null=True)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    car_workshop = models.ForeignKey(CarWorkshop, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    bonus = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Model(models.Model):
    car_brand = models.CharField(max_length=100)
    country_of_production = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    car_power = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.car_brand} {self.model}"


class Automobile(models.Model):
    engine_number = models.CharField(max_length=30, unique=True)
    year_of_vehicle = models.PositiveSmallIntegerField()
    colour = models.CharField(max_length=30)
    state_number = models.CharField(max_length=30, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    auto_model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auto_model} - {self.state_number}"


class Contract(models.Model):
    order_date = models.DateField()
    order_status = models.CharField(max_length=40)
    payment_status = models.CharField(max_length=40)
    date_of_acceptance_for_repair = models.DateField()
    scheduled_date_end_of_repair = models.DateField(blank=True, null=True)
    actual_date_end_of_repair = models.DateField(blank=True, null=True)
    total_payment = models.PositiveIntegerField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    auto = models.ForeignKey(Automobile, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Contract #{self.id} - {self.client.full_name}"



# Услуга
class Service(models.Model):
    type_of_repair = models.CharField(max_length=50)
    category_repair = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.type_of_repair


class Detail(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    country_of_manufacturer = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class DetailInService(models.Model):
    number_of_details = models.PositiveIntegerField()
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.detail.name} - {self.number_of_details}"


class DistributionOfWork(models.Model):
    status = models.CharField(max_length=20)
    start_date = models.DateField()
    scheduled_end_date = models.DateField(blank=True, null=True)
    actual_end_date = models.DateField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    quantity_of_services = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Work: {self.status} for Contract #{self.contract.id}"


class CarDetail(models.Model):
    automobile = models.ForeignKey('Automobile', on_delete=models.CASCADE, related_name="details")
    detail = models.ForeignKey('Detail', on_delete=models.CASCADE, related_name="cars")

    def __str__(self):
        return f"CarDetail: {self.automobile} - {self.detail}"


class DetailsFromClient(models.Model):
    detail = models.ForeignKey('Detail', on_delete=models.CASCADE, related_name="client_details")
    distribution = models.ForeignKey('DistributionOfWork', on_delete=models.CASCADE, related_name="client_details", blank=True, null=True)
    amount_of_detail = models.PositiveBigIntegerField()
    supplier = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"DetailsFromClient: {self.detail.name} - {self.amount_of_detail} pcs"
