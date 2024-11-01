from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)


class Conference(models.Model):
    title = models.CharField(max_length=300)
    themes = models.TextField(help_text="Список тем конференции")
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    location_description = models.TextField()

    def __str__(self):
        # Отображать название конференции и даты проведения
        return f"{self.title} ({self.start_date} - {self.end_date})"


class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Отображать пользователя, конференцию и оценку
        return f"Review by {self.user} for {self.conference} (Rating: {self.rating})"


class Participant(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False)

    def __str__(self):
        # Отображать пользователя и конференцию
        return f"{self.user} - {self.conference}"


class Results(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Result"  # Название в единственном числе
        verbose_name_plural = "Results"  # Название во множественном числе

    def __str__(self):
        # Отображать участника и статус принятия
        status = "Accepted" if self.accepted else "Not Accepted"
        return f"{self.participant} - {status}"
