from django.contrib import admin
from .models import Class, Discipline, Task, Grade, SchoolUser


class SchoolUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'class_id']


class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'year']


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'issue_date', 'due_date', 'discipline_id', 'class_id', 'teacher_id']


class GradeAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'schooluser_id', 'answer', 'submission_date', 'number']


admin.site.register(SchoolUser, SchoolUserAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Grade, GradeAdmin)
