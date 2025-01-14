from django.db import models
from django.contrib.auth.models import User


# Конференция
class Conference(models.Model):
    title = models.CharField(max_length=255)
    topics = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    participation_conditions = models.TextField()

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.review_set.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / reviews.count(), 2)
        return 0


# Регистрация участников на конференцию
class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    date_registered = models.DateTimeField(auto_now_add=True)
    presentation_topic = models.CharField(max_length=300)
    result = models.CharField(max_length=100,
                              choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
                              default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.conference.title}"


# Отзывы о конференции
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.conference.title}"
