from django.contrib.auth.models import User
from django.db import models


class Performer(models.Model):
    name = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Concert(models.Model):
    STATUS_CHOICES = [
        ('held', 'Проведен'),
        ('cancelled', 'Отменен'),
        ('prepared', 'Подготовлен'),
        ('in_progress', 'В работе')
    ]

    image = models.ImageField(upload_to='concerts', default='concerts.jpg')
    title = models.CharField(max_length=255)
    description = models.TextField()
    performer = models.ForeignKey(Performer, on_delete=models.CASCADE, related_name="concerts")
    date = models.DateField()
    age_limit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='in_progress')

    def __str__(self):
        return self.title


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ConcertEquipment(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="equipment")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="concerts")
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('concert', 'equipment')


class Ticket(models.Model):
    concert = models.ForeignKey('Concert', on_delete=models.CASCADE, related_name='ticket_categories')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    sold_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('concert', 'name')

    def __str__(self):
        return f"{self.name} ({self.concert.title})"

    @property
    def available_quantity(self):
        return self.total_quantity - self.sold_quantity

    def sell_tickets(self, quantity):
        if quantity > self.available_quantity:
            raise ValueError("Недостаточно доступных билетов")
        self.sold_quantity += quantity
        self.save()


class Order(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Подтверждено'),
        ('pending', 'В ожидании'),
        ('returned', 'Возврат'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.ticket.price
        super().save(*args, **kwargs)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="employee")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Organizer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="organized_concerts")
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name="organizers")

    class Meta:
        unique_together = ('employee', 'concert')
