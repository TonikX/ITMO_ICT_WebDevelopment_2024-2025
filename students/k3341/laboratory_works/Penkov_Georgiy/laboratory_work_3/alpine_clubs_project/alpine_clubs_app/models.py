from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="cities", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name}, {self.country}"


class Mountain(models.Model):
    name = models.CharField(max_length=100)
    elevation = models.PositiveSmallIntegerField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="mountains"
    )
    region = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.elevation}m, {self.country})"


class Route(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration_days = models.PositiveSmallIntegerField(null=True, blank=True)
    mountain = models.ForeignKey(
        Mountain, on_delete=models.CASCADE, related_name="routes", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} (mt {self.mountain.name})"


class Ascent(models.Model):
    planned_start_datetime = models.DateTimeField()
    planned_end_datetime = models.DateTimeField()
    actual_start_datetime = models.DateTimeField(null=True, blank=True)
    actual_end_datetime = models.DateTimeField(null=True, blank=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="ascents")
    is_successful = models.BooleanField(default=False)
    summary = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Ascent on {self.route.name} ({self.planned_start_datetime.date()})"


class Club(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="clubs", null=True, blank=True
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name="clubs", null=True, blank=True
    )
    contact_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class ClubMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clubs")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="members")
    join_datetime = models.DateTimeField(default=timezone.now)
    leave_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} in {self.club.name} (Joined: {self.join_datetime.date()})"


class AscentParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ascents")
    ascent = models.ForeignKey(
        Ascent, on_delete=models.CASCADE, related_name="participants"
    )
    is_successful = models.BooleanField(default=False)
    INCIDENT_TYPE = [
        ("INJ", "Injured"),
        ("MIS", "Missing"),
        ("FAT", "Fatality"),
    ]
    incident_type = models.CharField(
        max_length=100, choices=INCIDENT_TYPE, null=True, blank=True
    )
    incident_details = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} in {self.ascent}"
