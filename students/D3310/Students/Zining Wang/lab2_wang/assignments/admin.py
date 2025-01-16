# from django.contrib import admin
# from .models import Homework, Submission, Subject, Teacher


# admin.site.register(Homework)
# admin.site.register(Submission)
# admin.site.register(Subject)
# admin.site.register(Teacher)


from django.contrib import admin
from .models import Homework, Submission, Subject, Teacher

# 定制 Homework 模型的后台界面
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher', 'issue_date', 'due_date', 'description']
    search_fields = ['subject__name', 'description']
    list_filter = ['subject', 'teacher', 'issue_date', 'due_date']

# 定制 Teacher 模型的后台界面
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject']
    search_fields = ['user__username', 'subject__name']

# 注册模型
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Submission)
admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
