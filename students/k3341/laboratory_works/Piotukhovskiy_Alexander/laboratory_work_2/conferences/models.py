from django.contrib.auth.models import User
from django.db import models


class Conference(models.Model):
    title = models.CharField(max_length=200)
    topics = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    participation_conditions = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_conferences")
    participants = models.ManyToManyField(User, related_name="conferences_participated", blank=True)

    publication_recommended = models.BooleanField(
        "Рекомендована к публикации", null=True, blank=True,
        help_text="Отметьте, если конференция рекомендована к публикации"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ConferenceRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="ratings")
    review = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    class Meta:
        unique_together = ('user', 'conference')

    def __str__(self):
        return f"{self.user.username} - {self.rating} for {self.conference.title}"
