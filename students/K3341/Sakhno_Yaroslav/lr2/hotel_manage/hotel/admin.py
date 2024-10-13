from django.contrib import admin

from .models import Hotel, Room, HotelForm, RoomForm


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    form = HotelForm


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    form = RoomForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields["hotel"].widget.can_add_related = False
        return form
