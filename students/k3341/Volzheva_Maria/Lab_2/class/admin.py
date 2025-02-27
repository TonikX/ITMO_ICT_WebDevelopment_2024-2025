from django.contrib import admin
from . import models


admin.site.register(models.User)
admin.site.register(models.Assignment)
admin.site.register(models.Subject)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_text', 'submission_date', 'grade']
    list_filter = ['assignment', 'student']
    search_fields = ['student__username', 'assignment__subject__name']
    readonly_fields = ['assignment', 'student', 'submitted_text', 'submission_date']

    def has_change_permission(self, request, obj=None):

        if request.user.role == 'teacher' or request.user.is_superuser:
            return True
        return False


admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.Class)
