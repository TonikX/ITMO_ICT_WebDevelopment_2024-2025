from django.contrib import admin
from warriors.models import Warrior, Skill, Profession, SkillOfWarrior

admin.site.register(Warrior)
admin.site.register(Skill)
admin.site.register(Profession)
admin.site.register(SkillOfWarrior)
