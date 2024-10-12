from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    exclude = ('author',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user.username
        super().save_model(request, obj, form, change)


admin.site.register(Task, TaskAdmin)
