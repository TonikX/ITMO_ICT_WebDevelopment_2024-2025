from django.db import models

from users.models import User
from tours.models import Departure, Tour

# Create your models here.
class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    departure = models.ForeignKey(Departure, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} about {self.departure}'