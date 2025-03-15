from django.contrib import admin
from .models import Attribute, Skill, Character, CharactersAttribute, CharactersSkill

class CharactersAttributeInline(admin.TabularInline):
    model = CharactersAttribute
    extra = 1  # Количество пустых форм, которые будут показаны

class CharactersSkillInline(admin.TabularInline):
    model = CharactersSkill
    extra = 1  # Количество пустых форм, которые будут показаны

class CharacterAdmin(admin.ModelAdmin):
    inlines = (CharactersAttributeInline, CharactersSkillInline)

# Register your models here.
admin.site.register(Character, CharacterAdmin)
admin.site.register(Skill)
admin.site.register(Attribute)
admin.site.register(CharactersAttribute)
admin.site.register(CharactersSkill)

# Register your models here.
