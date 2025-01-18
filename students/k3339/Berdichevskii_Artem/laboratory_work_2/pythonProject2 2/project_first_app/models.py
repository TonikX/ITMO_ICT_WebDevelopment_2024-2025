from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    def __str__(self):
        return self.username


class Conference(models.Model):
    title = models.CharField(max_length=255)
    themes = models.TextField(help_text="Список тематик через запятую")
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    location_description = models.TextField()

    def __str__(self):
        return self.title


class Review(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    date_added = models.DateTimeField(auto_now_add=True)  # Дата добавления

    def __str__(self):
        return f"Review by {self.user} for {self.conference}"


class Participant(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f"{self.user.username} - {self.conference.title}"


class PresentationResult(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='results')
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Result for {self.participant.user.username} - {'Accepted' if self.is_accepted else 'Rejected'}"