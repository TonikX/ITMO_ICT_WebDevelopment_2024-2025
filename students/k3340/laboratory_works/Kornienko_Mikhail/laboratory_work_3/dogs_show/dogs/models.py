import uuid
from django.db import models


class Owner(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, null=True, blank=True)
    passport_details = models.TextField()
    contact_info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField()
    class_name = models.CharField(max_length=255)
    club_name = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    pedigree_document_number = models.CharField(max_length=255)
    sire_name = models.CharField(max_length=255)
    dam_name = models.CharField(max_length=255)
    date_of_last_vaccination = models.DateField()
    disqualified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Show(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    date = models.DateField()
    type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    sponsor = models.CharField(max_length=255)
    ring_schedule = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Participation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='participations')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='participations')
    participation_type = models.CharField(max_length=255)
    medical_exam_passed = models.BooleanField(default=False)
    payment_made = models.BooleanField(default=False)
    medal = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Expert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    club_name = models.CharField(max_length=255)
    rings_assigned = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Grade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='grades')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='grades')
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)