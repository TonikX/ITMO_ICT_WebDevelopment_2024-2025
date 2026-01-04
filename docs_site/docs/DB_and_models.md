# Этап 1. Проектирование базы данных и моделей Django

## Структура базы данных

Связи между сущностями:

```text
Hotel (1) ───< Room (∞)
Room (1) ───< Booking (∞) >───(1) User
Room (1) ───< Review (∞) >───(1) User
Room (M) ───< (M) Amenity
```

## Модель Hotel
```python
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_hotels')
    address = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
```
## Модель Room
```python
class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Одноместный'),
        ('double', 'Двухместный'),
        ('suite', 'Люкс'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    amenities = models.ManyToManyField('Amenity', related_name='rooms')
```

## Модель Booking
```python
class Booking(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Забронировано'),
        ('checked_in', 'Заселён'),
        ('checked_out', 'Выселен')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
```

## Модель Review
```python
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviews')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    stay_from = models.DateField()
    stay_to = models.DateField()
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
