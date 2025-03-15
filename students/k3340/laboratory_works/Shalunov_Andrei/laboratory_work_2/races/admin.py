from django.contrib import admin
from .models import Racer, Race, Automobile, Registration, Comment, RaceResult


class RacerAdmin(admin.ModelAdmin):
    list_display = ('user', 'team_name', 'experience', 'racer_class')
    search_fields = ('user__username', 'team_name', 'racer_class')
    filter_horizontal = ('cars',)


admin.site.register(Racer, RacerAdmin)
admin.site.register(Race)
admin.site.register(Automobile)
admin.site.register(Registration)
admin.site.register(Comment)
admin.site.register(RaceResult)
