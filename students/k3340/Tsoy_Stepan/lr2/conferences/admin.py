from django.contrib import admin
from django.utils.html import format_html
from .models import Conference, Speaker, Registration, Review

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'due_register')
    search_fields = ('title', 'description')
    list_filter = ('event_date',)

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('speaker', 'topic', 'conference', 'confirmed', 'approved', 'approve_button', 'confirm_button')
    list_editable = ('confirmed', 'approved')
    list_filter = ('confirmed', 'approved', 'conference')
    search_fields = ('speaker__username', 'topic')

    actions = ['mass_approve_speakers', 'mass_confirm_speakers']

    def mass_approve_speakers(self, request, queryset):
        count = queryset.update(approved=True)
        self.message_user(request, f"{count} speakers approved.")
    mass_approve_speakers.short_description = "✅ Mass approve selected speakers"

    def mass_confirm_speakers(self, request, queryset):
        count = queryset.update(confirmed=True)
        self.message_user(request, f"{count} speakers confirmed.")
    mass_confirm_speakers.short_description = "🎤 Mass confirm selected speakers"

    def approve_button(self, obj):
        if obj.approved is None:
            return format_html('<a class="button" href="approve/{}/">✅ Approve</a>', obj.pk)
        elif obj.approved:
            return format_html('<span style="color:green;">✔ Approved</span>')
        else:
            return format_html('<span style="color:red;">❌ Rejected</span>')
    approve_button.short_description = 'Approval'

    def confirm_button(self, obj):
        if not obj.confirmed:
            return format_html('<a class="button" href="confirm/{}/">🎤 Confirm</a>', obj.pk)
        return format_html('<span style="color:blue;">✔ Confirmed</span>')
    confirm_button.short_description = 'Participation'

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'conference', 'dt_register')
    list_filter = ('conference',)
    search_fields = ('user__username', 'conference__title')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('registration', 'rating', 'text')
    list_filter = ('rating',)
    search_fields = ('registration__user__username', 'text')

RegistrationAdmin.inlines = [ReviewInline]
