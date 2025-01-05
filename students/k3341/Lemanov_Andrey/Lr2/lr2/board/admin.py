from django.contrib import admin

from .models import Task, Student, Assignment, Class


admin.site.register(Assignment)
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(Class)
