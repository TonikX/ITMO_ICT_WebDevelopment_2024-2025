# Модели

## Туроператор

```python
class TravelAgency(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name
```

Хранит название фирмы и контакты.

## Тур

```python
class Tour(models.Model):
    hotel = models.CharField(max_length=200)
    stars = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Number of stars from 1 to 5"
    )
    agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, related_name="tours")
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_conditions = models.TextField()

    def __str__(self):
        return f"{self.hotel} ({self.stars} stars) - {self.agency.name}"

    def get_absolute_url(self):
        return reverse('tour_detail', args=[str(self.id)])

    def get_base_price(self):
        # Определяем минимальную стоимость тарифа и питания
        tariffs = self.tariffs.all()
        meal_options = self.meal_options.all()

        if tariffs.exists() and meal_options.exists():
            min_tariff_price = min(tariffs, key=lambda tariff: tariff.price).price
            min_meal_option_price = min(meal_options, key=lambda meal: meal.price).price
            return min_tariff_price + min_meal_option_price
        return 0
```

Хранит данные о туре (отель, его звездность, туроператор, страна, город, описание, даты, условия оплаты). Имеет метод по определению минимальной стоимсти тура)

## Тариф

```python
class Tariff(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tariffs")
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('tour', 'name')

    def __str__(self):
        return f"{self.name} - {self.price} RUB"
```

Хранит данные о предоставляемых для тура тарифах и их стоимости. Связана с туром.

## Опции питания

```python
class MealOption(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="meal_options")
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('tour', 'name')

    def __str__(self):
        return f"{self.name} - {self.price} RUB"
```

Хранит данные о доступных для тура опциях питания. Связана с туром.

## Бронирование

```python
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")
    num_people = models.PositiveIntegerField(default=1)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)
    meal_option = models.ForeignKey(MealOption, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)
    total_price = models.PositiveIntegerField(default=0)
    created = models.DateField(auto_now_add=True, null=True)

    def calculate_price(self):
        # Рассчитываем стоимость бронирования с учетом количества людей
        tariff_price = self.tour.get_base_price()
        total_price = tariff_price * self.num_people
        return round(total_price, 3)

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.tour.hotel}"
```

Хранит информацию о бронировании пользователя (турб количество человек, выбранный тариф, выбраный вариант питания, итоговая цена, статус и время создания брони)

Связана с туром, пользователем, тарифом и опциями питания. Имеет метод для посчета стоимости бронирования.

## Отзыв

```python
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Review by {self.user.username} ({self.rating}/10)"
```

Хранит отзывы пользователей. Связана с пользователем и туром.