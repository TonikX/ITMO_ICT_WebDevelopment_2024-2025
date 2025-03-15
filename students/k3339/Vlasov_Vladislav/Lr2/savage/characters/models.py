from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Attribute(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=15)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=50, default="", blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    #Особые поля
    bennies = models.SmallIntegerField(default=3, blank=True)

    wounds = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)], blank=True)
    fatigue = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], blank=True)

    
    #Описание
    appearance = models.TextField(null=True, blank=True)
    slogan = models.TextField(null=True, blank=True)

    #Статы
    attributes = models.ManyToManyField(Attribute, through="CharactersAttribute", blank=True)

    #Навыки
    skills = models.ManyToManyField(Skill, through="CharactersSkill", blank=True)

    def __str__(self) -> str:
        return self.name


class CharactersAttribute(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    bonus = models.SmallIntegerField(default=0)


class CharactersSkill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    bonus = models.SmallIntegerField()