from django.contrib import admin

from hh.models import CustomUser, Company, Vacancy, Skill, Tag, Application

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Tag)
admin.site.register(Skill)
admin.site.register(Application)