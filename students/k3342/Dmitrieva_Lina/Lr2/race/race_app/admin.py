from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Team, Racer, Race, Registration, RaceResult, RaceComment
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('passport_number', 'home_address', 'nationality')}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(Racer)
admin.site.register(Race)
admin.site.register(Registration)
admin.site.register(RaceResult)
admin.site.register(RaceComment)
