from django.db import models


class Agency(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Broker(models.Model):
    name = models.CharField(max_length=30)
    fixed_monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='brokers')

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    production_date = models.DateField()
    expiration_date = models.DateField()
    unit = models.CharField(max_length=50)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Batch(models.Model):
    SUPPLY_CONDITIONS_CHOICES = [
        ('prepayment', 'Prepayment'),
        ('no_prepayment', 'No Prepayment'),
    ]
    supply_conditions = models.CharField(max_length=20, choices=SUPPLY_CONDITIONS_CHOICES)
    contract_date = models.DateField()
    shipment_date = models.DateField()
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='batches')

    def __str__(self):
        return f'Batch {self.id}'


class BatchProduct(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='batch_products')
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in Batch {self.batch.id}'


class Client(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=10)
    registration_date = models.DateField()

    def __str__(self):
        return self.name


class ClientPurchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='purchases')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.IntegerField()
    purchase_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Purchase {self.id} by {self.client.name}'


class Transaction(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='transactions')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()

    def __str__(self):
        return f'Transaction {self.id}'
