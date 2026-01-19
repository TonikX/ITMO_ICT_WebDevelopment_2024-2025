from django.contrib import admin
from django.utils.html import format_html
from .models import Group, Classroom, Teacher, Subject, Student, Schedule, Grade


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_name', 'course', 'student_count', 'active_student_count']
    list_filter = ['course']
    search_fields = ['group_name']

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = 'Всего студентов'

    def active_student_count(self, obj):
        return obj.students.filter(status='active').count()

    active_student_count.short_description = 'Активных'


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['classroom_number', 'building', 'capacity', 'teacher_count', 'is_occupied']
    list_filter = ['building']
    search_fields = ['classroom_number', 'building']

    def teacher_count(self, obj):
        return obj.teachers.count()

    teacher_count.short_description = 'Преподавателей'

    def is_occupied(self, obj):
        return obj.teachers.exists()

    is_occupied.boolean = True
    is_occupied.short_description = 'Занят'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'position', 'classroom_link', 'schedule_count']
    list_filter = ['position', 'classroom__building']
    search_fields = ['last_name', 'first_name', 'patronymic']

    def classroom_link(self, obj):
        if obj.classroom:
            return format_html(
                '<a href="/admin/main/classroom/{}/change/">{}</a>',
                obj.classroom.classroom_id,
                str(obj.classroom)
            )
        return "—"

    classroom_link.short_description = 'Кабинет'

    def schedule_count(self, obj):
        return obj.schedules.count()

    schedule_count.short_description = 'Занятий'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_code', 'subject_name', 'hours_total', 'teacher_count', 'group_count']
    search_fields = ['subject_code', 'subject_name']

    def teacher_count(self, obj):
        return obj.schedules.values('teacher').distinct().count()

    teacher_count.short_description = 'Преподавателей'

    def group_count(self, obj):
        return obj.schedules.values('group').distinct().count()

    group_count.short_description = 'Групп'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'group_link', 'enrollment_date', 'status', 'average_grade']
    list_filter = ['status', 'group__course', 'enrollment_date']
    search_fields = ['last_name', 'first_name', 'patronymic', 'group__group_name']

    def group_link(self, obj):
        return format_html(
            '<a href="/admin/main/group/{}/change/">{}</a>',
            obj.group.group_id,
            obj.group.group_name
        )

    group_link.short_description = 'Группа'

    def average_grade(self, obj):
        avg = obj.grades.aggregate(Avg('grade_value'))['grade_value__avg']
        if avg:
            return f"{avg:.2f}"
        return "—"

    average_grade.short_description = 'Средний балл'


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['group', 'subject', 'teacher', 'classroom', 'day_of_week_display', 'lesson_number', 'semester',
                    'academic_year']
    list_filter = ['day_of_week', 'semester', 'academic_year', 'group__course']
    search_fields = ['group__group_name', 'subject__subject_name', 'teacher__last_name']

    def day_of_week_display(self, obj):
        return obj.get_day_of_week_display()

    day_of_week_display.short_description = 'День недели'


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'grade_value', 'grade_type_display', 'semester', 'academic_year',
                    'date_received']
    list_filter = ['grade_type', 'semester', 'academic_year', 'subject']
    search_fields = ['student__last_name', 'student__first_name', 'subject__subject_name']

    def grade_type_display(self, obj):
        return obj.get_grade_type_display()

    grade_type_display.short_description = 'Тип оценки'