# conferences/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from conference import settings

class Conference(models.Model):
    name = models.CharField("Название конференции", max_length=255)
    topics = models.TextField("Тематики", help_text="Перечислите тематики конференции через запятую")
    location = models.CharField("Место проведения", max_length=255)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    description = models.TextField("Описание конференции")
    location_description = models.TextField("Описание места проведения")
    participation_conditions = models.TextField("Условия участия")
    recommended_for_publication = models.BooleanField(
        "Рекомендовано к публикации",
        null=True,
        blank=True,
        help_text="Администратор может указать результат выступления"
    )

    def __str__(self):
        return self.name

class AuthorRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    presentation_title = models.CharField("Название выступления", max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} – {self.conference.name}"

class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment_text = models.TextField("Текст отзыва")
    rating = models.IntegerField("Рейтинг", validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment_date = models.DateTimeField("Дата отзыва", auto_now_add=True)

    def __str__(self):
        return f"Отзыв от {self.user.username} по {self.conference.name}"