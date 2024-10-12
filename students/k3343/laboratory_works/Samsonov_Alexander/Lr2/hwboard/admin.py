from django.contrib import admin

from .models import Task, Student, Assignment
from datetime import date


class TaskAdmin(admin.ModelAdmin):
    exclude = ('author', 'issue_date')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user.username
            obj.issue_date = date.today()
        super().save_model(request, obj, form, change)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class')
    list_filter = ('student_class',)
    readonly_fields = ('name', 'email')
    fields = ('name', 'email', 'student_class')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(student_class__isnull=True)


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('task_title', 'student_name', 'date_hand_in')
    readonly_fields = ('text', 'task', 'student', 'task_penalties', 'date_hand_in')
    fields = ('task', 'student', 'text', 'date_hand_in', 'grade', 'task_penalties')


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_authenticated:
            return qs.filter(task__author=request.user, grade__isnull=True)
        return qs.none()

    def task_title(self, obj):
        return obj.task.title

    def student_name(self, obj):
        return obj.student.name

    def task_penalties(self, obj):
        return obj.task.penalties

    task_title.short_description = 'Task title'
    student_name.short_description = 'Student name'

    def save_model(self, request, obj, form, change):
        obj.date_grade = date.today()
        obj.status = 'gr'
        super().save_model(request, obj, form, change)

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Task, TaskAdmin)
