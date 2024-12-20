from django.contrib.auth.models import User
from django.db import models
from rest_framework.exceptions import ValidationError


class Agency(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    legal_address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name} Agency'


class BrokerCompany(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    monthly_fee = models.IntegerField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.agency.name} broker company'


class Broker(User):

    class Meta:
        proxy = True
        verbose_name = 'Broker'
        verbose_name_plural = 'Brokers'

    def __str__(self):
        return f'{self.username} broker'


class BrokerInfo(models.Model):
    broker = models.OneToOneField(Broker, on_delete=models.CASCADE)
    broker_company = models.ForeignKey(BrokerCompany,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True)
    monthly_fee = models.IntegerField()
    contact_number = models.CharField(max_length=20)


class ProductGroup(models.Model):
    group = models.CharField(max_length=100)


class Manufacturer(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)

    production_date = models.DateField()
    expiry_period = models.PositiveIntegerField(null=True, blank=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.manufacturer.name} product: {self.name}'

    def clean(self):
        if self.quantity < 0:
            raise ValidationError('Quantity cannot be negative')


class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('op', "Opened"),
        ('ap', "Approved"),
        ('p', 'Paid'),
        ('d', 'Delivered')
    )
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE)
    prepaid = models.BooleanField(default=False)
    delivery_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=5, choices=ORDER_STATUS_CHOICES, default='op')

    @property
    def total_cost(self):
        return self.batchproduct_set.aggregate(models.Sum('batch_price'))['batch_price__sum']

    @property
    def total_paid(self):
        return self.transaction_set.aggregate(models.Sum('amount'))['amount__sum']


class Transaction(models.Model):
    STATUS_CHOICES = (
        ('cr', 'Created'),
        ('ip', 'In Progress'),
        ('cf', 'Confirmed'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.FloatField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)


class BatchProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.FloatField()

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError("Batch quantity cannot exceed product quantity.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def batch_price(self):
        return self.quantity * self.price_per_unit

