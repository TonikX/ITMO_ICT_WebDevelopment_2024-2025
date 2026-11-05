from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.username} ({self.get_full_name() or 'Без имени'})"

    def get_absolute_url(self):
        return reverse('detail', kwargs={ 'pk': self.pk })