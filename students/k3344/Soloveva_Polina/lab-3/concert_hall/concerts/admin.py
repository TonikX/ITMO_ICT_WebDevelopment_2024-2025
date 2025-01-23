from django.contrib import admin
from .models import Performer, Concert, Equipment, ConcertEquipment, Ticket, Order, Employee, Organizer


class PerformerAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'email', 'phone')
    search_fields = ('name', 'manager', 'email')
    list_filter = ('manager',)
    ordering = ('name',)


class ConcertAdmin(admin.ModelAdmin):
    list_display = ('title', 'performer', 'date', 'status', 'age_limit')
    search_fields = ('title', 'performer__name')
    list_filter = ('status', 'date', 'performer')
    ordering = ('date',)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


class ConcertEquipmentAdmin(admin.ModelAdmin):
    list_display = ('concert', 'equipment', 'quantity')
    search_fields = ('concert__title', 'equipment__name')
    list_filter = ('concert', 'equipment')
    ordering = ('concert',)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'concert', 'price', 'total_quantity', 'sold_quantity', 'available_quantity')
    search_fields = ('name', 'concert__title')
    list_filter = ('concert', 'price')
    ordering = ('concert', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticket', 'quantity', 'date', 'total_price', 'status')
    search_fields = ('user__username', 'ticket__name', 'status')
    list_filter = ('status', 'date')
    ordering = ('date',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'salary', 'phone', 'email')
    search_fields = ('name', 'position')
    list_filter = ('position',)
    ordering = ('name',)


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('employee', 'concert')
    search_fields = ('employee__name', 'concert__title')
    list_filter = ('concert',)
    ordering = ('concert',)


admin.site.register(Performer, PerformerAdmin)
admin.site.register(Concert, ConcertAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(ConcertEquipment, ConcertEquipmentAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Organizer, OrganizerAdmin)

