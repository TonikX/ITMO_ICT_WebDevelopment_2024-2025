from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Ingredients(models.Model):
    UNIT_CHOICES = [
        ('liters', 'Liters (L)'),
        ('grams', 'Grams (g)'),
        ('units', 'Units'),  # 1 egg, for example
        ('pinches', 'Pinches'),
    ]

    ingredient_name = models.CharField(max_length=100)
    quantity_si = models.FloatField()
    unit_si = models.CharField(max_length=20, choices=UNIT_CHOICES)

    def __str__(self):
        return f"{self.ingredient_name}: {self.quantity_si} {self.unit_si}"


class Tags(models.Model):
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.tag_name}"


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'ez'),
        ('Normal', 'nl'),
        ('Hard', 'hd'),
    ]

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=500)
    thumbnail_link = models.CharField(max_length=500)
    content_json = models.JSONField()
    time_takes = models.TimeField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    dt_update = models.DateTimeField(auto_now_add=True)

    # to calculate avg rating fast. Updated on addition of comment
    stars_sum = models.IntegerField(default=0)
    number_ratings = models.IntegerField(default=0)

    tags = models.ManyToManyField(Tags)
    ingredients = models.ManyToManyField(Ingredients)

    def __str__(self):
        return f"{self.header}"


class CuratedList(models.Model):
    Curator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    header = models.CharField(max_length=500)
    content_json = models.JSONField()
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return f"{self.header}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Rating must be between 1 and 10"
    )

    header = models.CharField(max_length=500)
    content_text = models.TextField(blank=False)

    dt_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.header} by {self.author.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
