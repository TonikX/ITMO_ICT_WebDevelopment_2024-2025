from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Race(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(null=False, default='12:00')
    result = models.CharField(max_length=200, null=False, default='Неизвестен')

    def __str__(self):
        return self.name

class Registration(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('race', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.race.name}"

class Comment(models.Model):
    COMMENT_TYPES = [
        ('positive', 'Положительный'),
        ('negative', 'Отрицательный'),
    ]

    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    comment_type = models.CharField(max_length=10, choices=COMMENT_TYPES)
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        help_text="Enter a rating between 1 and 10."
    )

    def __str__(self):
        return f"{self.user.username} - {self.race.name} - {self.comment_type}"
