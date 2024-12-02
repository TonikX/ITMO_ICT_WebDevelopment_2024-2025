from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.username


class Recipe(models.Model):
    COMPLEXITY_CHOICES = [
        ('easy', 'Легко'),
        ('medium', 'Средне'),
        ('hard', 'Трудно'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    complexity = models.CharField(max_length=50, choices=COMPLEXITY_CHOICES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipes', on_delete=models.CASCADE)
    image_urls = models.JSONField()
    video_url = models.URLField(blank=True, null=True)
    average_rating = models.FloatField(default=0)

    def str(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def str(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='recipes', on_delete=models.CASCADE)

    def str(self):
        return f'{self.recipe.title} - {self.tag.name}'


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'Comment by {self.user.username} on {self.recipe.title}'


class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='saved_recipes', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, related_name='saved_by', on_delete=models.CASCADE)

    def str(self):
        return f'{self.user.username} saved {self.recipe.title}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    chef = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribers', on_delete=models.CASCADE)

    def str(self):
        return f'{self.subscriber.username} follows {self.chef.username}'


class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ratings', on_delete=models.CASCADE)
    rating_value = models.PositiveSmallIntegerField()

    def str(self):
        return f'Rating {self.rating_value} by {self.user.username} for {self.recipe.title}'