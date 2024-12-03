from django.contrib.auth.models import AbstractUser
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('job_seeker', 'Job Seeker'),
        ('hr', 'HR'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='job_seeker')
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.username

class Tag(models.Model):
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class Skill(models.Model):
    skill = models.CharField(max_length=255)

    def __str__(self):
        return self.skill


class CV(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content_blob = models.TextField()

    def __str__(self):
        return self.author.username


class Vacancy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    salary = models.IntegerField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag)
    skills = models.ManyToManyField(Skill)

    def __str__(self):
        return self.title


class Application(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    CV = models.ForeignKey(CV, on_delete=models.CASCADE)
    message = models.TextField()
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vacancy.title} by {self.applicant.username}'
