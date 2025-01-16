# # from django.db import models
# # from django.contrib.auth.models import User

# # class Subject(models.Model):
# #     name = models.CharField(max_length=100)
# #     teacher = models.CharField(max_length=100)

# #     def __str__(self):
# #         return self.name

# # class Homework(models.Model):
# #     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
# #     issue_date = models.DateField()
# #     due_date = models.DateField()
# #     description = models.TextField()
# #     penalty_info = models.TextField(blank=True, null=True)

# #     def __str__(self):
# #         return f"{self.subject.name} - {self.description[:50]}"

# # class HomeworkSubmission(models.Model):
# #     student = models.ForeignKey(User, on_delete=models.CASCADE)
# #     homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
# #     submission_date = models.DateField(auto_now_add=True)
# #     content = models.TextField()
# #     grade = models.IntegerField(blank=True, null=True)

# #     def __str__(self):
# #         return f"{self.student.username} - {self.homework.description[:50]}"


# from django.db import models
# from django.contrib.auth.models import User

# class Subject(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name


# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     subjects = models.ManyToManyField(Subject)

#     def __str__(self):
#         return self.user.username


# class Homework(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
#     issue_date = models.DateField(auto_now_add=True)
#     due_date = models.DateField()
#     description = models.TextField()
#     penalty = models.TextField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"{self.subject.name} - {self.description[:50]}"


# class Submission(models.Model):
#     homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     grade = models.CharField(max_length=10, blank=True, null=True)  # Grade can be assigned by teacher

#     def __str__(self):
#         return f"{self.student.username} - {self.homework.description[:50]}"


from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Homework(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100, null=True)
    # teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    description = models.TextField()
    penalty = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.description[:100]}"
    

# class Homework(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
#     issue_date = models.DateField()
#     due_date = models.DateField()
#     description = models.TextField()
#     penalty = models.TextField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return f"{self.subject.name} - {self.description[:100]}"


# class Homework(models.Model):
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     old_teacher = models.CharField(max_length=100, null=True, blank=True)  # 暂时保留原字段
#     teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True, blank=True)  # 新字段
#     issue_date = models.DateField()
#     due_date = models.DateField()
#     description = models.TextField()
#     penalty = models.TextField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return f"{self.subject.name} - {self.description[:100]}"


class Submission(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    submitted_at = models.DateTimeField()
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.homework.description[:50]}"
