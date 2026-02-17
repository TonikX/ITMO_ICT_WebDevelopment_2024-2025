# Админка Django

## Настройка админки

```python
# racing_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, Car, Race, RaceRegistration, Comment

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'experience', 'driver_class')
    list_filter = ('experience', 'driver_class', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('experience', 'driver_class', 'bio')
        }),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('model', 'owner', 'team', 'year')
    list_filter = ('team', 'year')
    search_fields = ('model', 'owner__username', 'team__name')
    ordering = ('model',)

@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'is_active')
    list_filter = ('is_active', 'date', 'location')
    search_fields = ('name', 'location')
    ordering = ('-date',)
    date_hierarchy = 'date'

@admin.register(RaceRegistration)
class RaceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('racer', 'race', 'registration_date', 'position', 'final_time')
    list_filter = ('race', 'registration_date', 'position')
    search_fields = ('racer__username', 'race__name')
    ordering = ('-registration_date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'race', 'type', 'rating', 'created_date', 'is_approved')
    list_filter = ('type', 'rating', 'is_approved', 'created_date')
    search_fields = ('author__username', 'race__name', 'text')
    ordering = ('-created_date',)
    actions = ['approve_comments', 'disapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Одобрить выбранные комментарии"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Отклонить выбранные комментарии"
```

## Возможности админки

### Управление пользователями
- Просмотр и редактирование профилей пользователей
- Управление уровнем опыта и классом гонщика
- Активация/деактивация учетных записей

### Управление гонками
- Создание и редактирование гонок
- Установка даты, времени и места проведения
- Активация/деактивация гонок

### Управление регистрациями
- Просмотр всех регистраций на гонки
- Установка результатов и позиций участников
- Фиксация финального времени

### Модерация комментариев
- Просмотр всех комментариев
- Одобрение/отклонение комментариев
- Фильтрация по типу и рейтингу

## Доступ к админке

1. Перейдите на `/admin/`
2. Введите учетные данные суперпользователя
3. Используйте меню для управления данными

## Рекомендации по использованию

- Регулярно проверяйте комментарии для модерации
- Своевременно устанавливайте результаты гонок
- Используйте фильтры для быстрого поиска информации