from django.contrib import admin
from .models import Conference, Review, Registration


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'is_published')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return ['user', 'conference']


admin.site.register(Registration, RegistrationAdmin)


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')


def delete_selected_reviews(modeladmin, request, queryset):
    queryset.delete()


delete_selected_reviews.short_description = "Удалить выбранные отзывы"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('conference', 'user', 'text', 'rating')
    list_filter = ('conference', 'user')
    search_fields = ('conference__name', 'user__username', 'text')
    actions = [delete_selected_reviews]