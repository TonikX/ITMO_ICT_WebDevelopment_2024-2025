from django.contrib import admin
from blog.models import Class, User, Subject, Homework, Submission


class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year')
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'student_class')
    list_filter = ('role', 'student_class')
    search_fields = ('username', 'first_name', 'last_name', 'phone_number')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('teachers',)


class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'assigned_date', 'due_date')
    list_filter = ('subject', 'teacher', 'assigned_date', 'due_date')
    search_fields = ('title', 'description')


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'homework', 'submission_date', 'grade')
    list_filter = ('homework', 'student', 'grade')
    search_fields = ('student__username', 'homework__title')


# Register your models here.
admin.site.register(Class, ClassAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Submission, SubmissionAdmin)
