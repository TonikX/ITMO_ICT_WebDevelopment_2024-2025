from django.contrib import admin
from .models import User, Homework, Submission

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'role', 'email')
    search_fields = ('first_name', 'last_name', 'email')


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'assigned_date', 'due_date')
    search_fields = ('subject',)
    list_filter = ('teacher',)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'homework', 'submission_date', 'grade')
    search_fields = ('student__last_name', 'homework__subject')
    list_filter = ('grade',)


admin.site.register(User, UserAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Submission, SubmissionAdmin)
