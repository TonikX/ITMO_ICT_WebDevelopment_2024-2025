from django.contrib import admin
from .models import UserProfile, Homework,Submission


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'role')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'issue_date', 'due_date', 'description', 'penalty_info')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('hw', 'student', 'submission_text', 'grade')
