    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.conf import settings
    
    
    class User(AbstractUser):
        class Role(models.TextChoices):
            STUDENT = "student", "Student"
            TEACHER = "teacher", "Teacher"
    
        role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    
    
    class Homework(models.Model):
        subject = models.CharField(max_length=100)
        teacher = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={"role": "teacher"}
        )
        assigned_date = models.DateField()
        due_date = models.DateField()
        description = models.TextField()
        penalties_info = models.TextField(blank=True, null=True)
    
        objects = models.Manager()
    
    
    class Submission(models.Model):
        homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
        student = models.ForeignKey(
            settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={"role": "student"}
        )
        submission_text = models.TextField()
        submission_date = models.DateField(auto_now_add=True)
        grade = models.IntegerField(blank=True, null=True)
    
        objects = models.Manager()