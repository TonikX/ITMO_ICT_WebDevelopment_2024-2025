from django.contrib import admin
from .models import User, Subject, Homework, GroupTeacher, StudyGroup, HomeworkSubmission, GradeHomework

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Homework)
admin.site.register(GroupTeacher)
admin.site.register(StudyGroup)
admin.site.register(HomeworkSubmission)
admin.site.register(GradeHomework)
