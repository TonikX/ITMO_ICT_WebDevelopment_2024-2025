from django.contrib import admin

from warriors_app import models

admin.site.register(models.Warrior)
admin.site.register(models.Profession)
admin.site.register(models.Skill)
admin.site.register(models.SkillOfWarrior)
