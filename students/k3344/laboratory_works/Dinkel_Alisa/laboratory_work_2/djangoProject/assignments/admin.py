from django.contrib import admin
from .models import Subject, Assignment, HomeworkSubmission
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'issue_date', 'due_date', 'assignment_status')
    list_filter = ('subject', 'teacher', 'assignment_status')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            return queryset.filter(teacher=request.user)
        return queryset


@admin.register(HomeworkSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submission_date', 'grade')
    list_editable = ('grade',)
    list_filter = ('assignment', 'student')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_staff:
            return queryset.filter(assignment__teacher=request.user)
        return queryset


# Функция для создания групп
def create_groups():
    teachers_group, _ = Group.objects.get_or_create(name='Учителя')
    students_group, _ = Group.objects.get_or_create(name='Ученики')

    # Получаем контент-тайпы моделей
    assignment_ct = ContentType.objects.get_for_model(Assignment)
    submission_ct = ContentType.objects.get_for_model(HomeworkSubmission)

    # Добавляем учителям нужные права
    teachers_group.permissions.set([
        Permission.objects.get(codename='add_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='change_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='delete_assignment', content_type=assignment_ct),
        Permission.objects.get(codename='view_assignment', content_type=assignment_ct),

        Permission.objects.get(codename='add_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='change_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='delete_homeworksubmission', content_type=submission_ct),
        Permission.objects.get(codename='view_homeworksubmission', content_type=submission_ct),
    ])


# create_groups()
