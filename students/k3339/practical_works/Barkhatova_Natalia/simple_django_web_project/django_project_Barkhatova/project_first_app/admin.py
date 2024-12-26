from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from project_first_app.models import Owner, Car, License, Owning, User

admin.site.register(Owner)
admin.site.register(Car)
admin.site.register(License)
admin.site.register(Owning)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('passport_number', 'home_address', 'nationality'),
        }),
    )


admin.site.register(User, CustomUserAdmin)
