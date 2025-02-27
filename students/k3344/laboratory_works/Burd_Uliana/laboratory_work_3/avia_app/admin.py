from django.contrib import admin
from .models import Aircraft, Flight, CrewMember, Employee


class CrewMemberInline(admin.TabularInline):
    model = CrewMember


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'seats', 'speed', 'carrier')
    inlines = [CrewMemberInline]


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'distance', 'departure_point', 'destination_point',
                    'departure_datetime', 'arrival_datetime', 'sold_tickets')


@admin.register(CrewMember)
class CrewMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'education', 'experience', 'passport_data', 'is_airport_employee')
