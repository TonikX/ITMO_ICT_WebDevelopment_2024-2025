from django.contrib import admin
from .models import *

admin.site.register(User)

admin.site.register(Criterion)
admin.site.register(Option)
admin.site.register(Submission)
admin.site.register(Review)

class CriterionInline(admin.TabularInline):
    model = Criterion
    extra = 4

class TaskAdmin(admin.ModelAdmin):
    inlines = [CriterionInline]

admin.site.register(Task, TaskAdmin)