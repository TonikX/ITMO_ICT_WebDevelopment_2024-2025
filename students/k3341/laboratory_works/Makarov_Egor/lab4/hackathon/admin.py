from django.contrib import admin
from .models import (
    Tag, Task, TaskResourceLink, TaskResourceFile,
    Team, TeamMember, Solution, SolutionAttachment, Evaluation
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

class TaskResourceLinkInline(admin.TabularInline):
    model = TaskResourceLink
    extra = 0

class TaskResourceFileInline(admin.TabularInline):
    model = TaskResourceFile
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "curator", "consultation_url", "created_at")
    search_fields = ("title",)
    inlines = (TaskResourceLinkInline, TaskResourceFileInline)

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "captain", "selected_task", "created_at")
    search_fields = ("name", "captain__username")
    inlines = (TeamMemberInline,)

class SolutionAttachmentInline(admin.TabularInline):
    model = SolutionAttachment
    extra = 0

@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "team", "task", "status", "created_at", "submitted_at")
    list_filter = ("status", "task")
    search_fields = ("title", "team__name")
    inlines = (SolutionAttachmentInline,)

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("id", "solution", "jury_member", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("solution__title", "jury_member__username")
