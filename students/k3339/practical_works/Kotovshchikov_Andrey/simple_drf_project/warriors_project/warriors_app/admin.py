from django.contrib import admin

from warriors_app.models import Warrior, Skill


class SkillInline(admin.TabularInline):
    model = Warrior.skill.through
    extra = 1


@admin.register(Warrior)
class WarriorAdmin(admin.ModelAdmin):
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin): ...
