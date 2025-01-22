from django.db import models
from django.utils import timezone


class Conference(models.Model):
    name = models.CharField(unique=True, max_length=512)
    start_date = models.DateField(null=False, default=timezone.now)
    end_date = models.DateField()
    is_registration_opened = models.BooleanField(default=True)
    free_places = models.IntegerField(default=0)
    description = models.TextField(null=False)
    participation_condition = models.TextField(null=False)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(free_places__gte=0), name='free_places >= 0')]
    def __str__(self):
        return f"Conference {self.name}"
