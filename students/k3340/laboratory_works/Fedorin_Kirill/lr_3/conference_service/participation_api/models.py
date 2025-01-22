from auth_api.models import UserAccount
from conference_api.models import Conference
from django.db import models
from django.utils import timezone


class Participation(models.Model):
    registration_date = models.DateField(null=False, default=timezone.now)
    from_town = models.CharField(max_length=30)
    publication_theme = models.TextField(max_length=2000)
    is_cancelled = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, related_name='participation')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, null=False, related_name='participation')

    def __str__(self):
        return f'Participation registered on {self.registration_date} by {self.client.firstname} {self.client.lastname}, conference {self.conference.name}'
