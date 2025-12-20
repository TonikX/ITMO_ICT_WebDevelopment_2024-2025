from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Ownership, Car, CarLicense, User

class CustomUserAdmin(UserAdmin):
    # Добавляем новые поля в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Информация о владельце автомобиля', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )
    
    # Добавляем новые поля в форму создания
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Информация о владельце автомобиля', {
            'fields': ('passport_number', 'home_address', 'nationality', 'birth_date')
        }),
    )
    
    # Добавляем новые поля в список пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'passport_number', 'home_address', 'nationality', 'is_staff')
    list_filter = ('nationality', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'passport_number', 'nationality')

class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1
    fields = ['car', 'start_date', 'end_date']
    verbose_name = 'Владение автомобилем'
    verbose_name_plural = 'Владения автомобилями'

class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'number', 'color', 'owners_count']
    search_fields = ['brand', 'model', 'number']

    def owners_count(self, obj):
        return obj.ownership_set.count()
    owners_count.short_description = 'Кол-во владельцев'

class UserAdminWithCars(CustomUserAdmin):
    inlines = [OwnershipInline]
    
    def cars_count(self, obj):
        return obj.ownership_set.count()
    cars_count.short_description = 'Кол-во автомобилей'
    
    list_display = CustomUserAdmin.list_display + ('cars_count',)

# Регистрируем модели
admin.site.register(User, UserAdminWithCars)
admin.site.register(Car, CarAdmin)
admin.site.register(CarLicense)
admin.site.register(Ownership)