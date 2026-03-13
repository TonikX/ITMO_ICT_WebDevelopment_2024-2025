from django.contrib import admin
from .models import Subject, Teacher, Homework, Submission, Grade

admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Homework)
admin.site.register(Submission)
admin.site.register(Grade)
