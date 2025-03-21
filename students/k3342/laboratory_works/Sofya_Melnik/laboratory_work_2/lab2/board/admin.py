from django.contrib import admin
from .models import User, Homework, Submission

# Register your models here.
admin.site.register(User)
admin.site.register(Homework)
admin.site.register(Submission)