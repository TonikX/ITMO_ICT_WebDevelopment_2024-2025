from django.contrib import admin

from .models import Teacher, Student, Subject, Grade, Lesson

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Lesson)