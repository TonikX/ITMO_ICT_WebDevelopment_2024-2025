from django.contrib import admin
from .models import Team, Car, Racer, Race, RaceParticipant, Comment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'team']


@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ['user_first_name', 'user_last_name', 'user', 'team', 'years_of_experience', 'participant_class']
    list_filter = ['status']

    @staticmethod
    def user_first_name(obj):
        return obj.user.first_name

    @staticmethod
    def user_last_name(obj):
        return obj.user.last_name

    user_first_name.short_description = 'Имя'
    user_last_name.short_description = 'Фамилия'


class RaceParticipantInline(admin.TabularInline):
    model = RaceParticipant
    extra = 1


@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'race_date', 'result']
    list_filter = ['race_date']
    inlines = [RaceParticipantInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'text', 'comment_type', 'rating', 'created_at')


admin.site.register(Comment, CommentAdmin)
