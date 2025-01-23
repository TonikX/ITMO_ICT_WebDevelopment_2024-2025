from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    pass


class TravelAgency(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name


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


class Tariff(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tariffs")
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('tour', 'name')

    def __str__(self):
        return f"{self.name} - {self.price} RUB"


class MealOption(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="meal_options")
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('tour', 'name')

    def __str__(self):
        return f"{self.name} - {self.price} RUB"


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


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="reviews")
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Review by {self.user.username} ({self.rating}/10)"
