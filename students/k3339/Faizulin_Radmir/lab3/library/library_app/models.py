from django.db import models
# from datetime import datetime
from django.utils import timezone

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    publishing_year = models.DateField()
    cipher = models.CharField(max_length=10)

    def __str__(self):
        return "{}, {}".format(self.author, self.name)


class Hall(models.Model):
    sequence_number = models.IntegerField()
    name = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return "number: {} {}".format(self.sequence_number, self.name)


class Copy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.book, self.hall)


class Reader(models.Model):
    EDUCATIONS = [
        ('0', 'no education'),
        ('1', 'elementary'),
        ('2', 'middle'),
        ('3', 'bachelor'),
        ('4', 'master')
    ]
    name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    passport = models.CharField(max_length=10)
    birth_date = models.DateField()
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    education = models.CharField(choices=EDUCATIONS, default='0', max_length=1)
    phd = models.BooleanField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    library_card_number = models.CharField(max_length=10)

    def __str__(self):
        return "{} {} {}".format(self.surname, self.name, self.second_name)


class Assignment(models.Model):
    copy = models.ForeignKey(Copy, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=timezone.now)
    date_returned = models.DateField(default=None, blank=True, null=True)