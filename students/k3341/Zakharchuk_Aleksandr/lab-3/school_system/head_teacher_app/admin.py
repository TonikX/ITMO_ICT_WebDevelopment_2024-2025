from django.contrib import admin

from head_teacher_app import models

admin.site.register(models.Room)
admin.site.register(models.Teacher)
admin.site.register(models.Subject)
admin.site.register(models.Class)
admin.site.register(models.Student)
admin.site.register(models.Schedule)
admin.site.register(models.Grade)


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_approved")
    list_filter = ("is_approved",)
    search_fields = ("user__username", "user__email")
