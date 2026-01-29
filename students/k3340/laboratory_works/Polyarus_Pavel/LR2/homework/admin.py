from django.contrib import admin
from .models import Subject, Class, Homework, Submission


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'get_students_count')
    list_filter = ('year',)
    search_fields = ('name',)
    filter_horizontal = ('students',)
    
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Кол-во студентов'


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at', 'deadline', 'is_overdue')
    list_filter = ('subject', 'teacher', 'created_at', 'deadline')
    search_fields = ('title', 'description')
    filter_horizontal = ('classes',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('subject', 'teacher', 'classes', 'title', 'description')
        }),
        ('Сроки и оценка', {
            'fields': ('deadline', 'max_score')
        }),
    )
    
    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Просрочено'


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'homework', 'submitted_at', 'grade', 'final_score', 'status', 'get_penalty')
    list_filter = ('status', 'homework__subject', 'submitted_at')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'homework__title')
    readonly_fields = ('submitted_at', 'calculate_penalty', 'final_score')
    date_hierarchy = 'submitted_at'
    
    fieldsets = (
        ('Информация о работе', {
            'fields': ('homework', 'student', 'submitted_at', 'answer_text')
        }),
        ('Оценивание', {
            'fields': ('grade', 'teacher_comment', 'status')
        }),
        ('Расчеты', {
            'fields': ('calculate_penalty', 'final_score'),
            'classes': ('collapse',)
        }),
    )
    
    def get_penalty(self, obj):
        return obj.calculate_penalty()
    get_penalty.short_description = 'Штраф'
    
    actions = ['mark_as_graded', 'mark_as_pending']
    
    def mark_as_graded(self, request, queryset):
        updated = queryset.update(status='graded')
        self.message_user(request, f'Обновлено {updated} работ(ы).')
    mark_as_graded.short_description = 'Отметить как проверенные'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'Обновлено {updated} работ(ы).')
    mark_as_pending.short_description = 'Отметить как непроверенные'


admin.site.site_header = 'Доска домашних заданий - Администрирование'
admin.site.site_title = 'Админ-панель'
admin.site.index_title = 'Управление системой'