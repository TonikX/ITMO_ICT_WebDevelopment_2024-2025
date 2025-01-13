from django.contrib import admin
from .models import Race, Registration, Comment, User

# Register your models here.
admin.site.register(Race)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(User)