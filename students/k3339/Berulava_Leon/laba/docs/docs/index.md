# Лабораторная работа

## Цель
Овладеть практическими навыками и умениями реализации web-сервисов средствами Django 2.2.

## Оборудование
Компьютерный класс.

## Программное обеспечение
- Python 3.6+
- Django 3
- PostgreSQL *

## Практическое задание
Реализовать сайт, используя фреймворк Django 3 и СУБД PostgreSQL *, в соответствии с вариантом задания лабораторной работы.

### Условие задания
Хранится информация о:
- названии тура,
- турагентстве,
- описании тура,
- периоде проведения тура,
- условиях оплаты.

### Необходимый функционал:
1. **Регистрация новых пользователей.**
2. **Просмотр и резервирование туров.**  
   Пользователь должен иметь возможность редактировать и удалять свои резервирования.
3. **Написание отзывов к турам.**  
   При добавлении комментариев должны сохраняться:
   - даты тура,
   - текст комментария,
   - рейтинг (1-10),
   - информация о комментаторе.
4. **Подтверждение резервирования тура через Django-admin.**
5. **Клиентская таблица:**  
   Должна формироваться таблица, отображающая все проданные туры по странам.

---

## Итоговые модели

Ваш проект включает следующие приложения: `tours`, `users`, `basket`.

### Модели проекта:

#### `Tour`

```python
class Tour(models.Model):
    name = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_terms = models.TextField()
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.tour.name} by {self.user.username}"

class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tour = models.ForeignKey(to=Tour, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tour.name}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.tour.price

    def __str__(self):
        return f"Booking: {self.tour.name} by {self.user.username}"

class User(AbstractUser):
    pass
