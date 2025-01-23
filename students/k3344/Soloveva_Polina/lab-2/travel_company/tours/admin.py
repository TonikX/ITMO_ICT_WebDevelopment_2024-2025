from django.contrib import admin
from .models import (
    CustomUser,
    TravelAgency,
    Tour,
    Tariff,
    MealOption,
    Booking,
    Review,
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(TravelAgency)
class TravelAgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'stars', 'agency', 'country', 'city', 'start_date', 'end_date')
    list_filter = ('stars', 'country', 'agency')
    search_fields = ('hotel', 'country', 'city')
    ordering = ('start_date',)


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tour')
    list_filter = ('tour',)
    search_fields = ('name',)
    ordering = ('price',)


@admin.register(MealOption)
class MealOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tour')
    list_filter = ('tour',)
    search_fields = ('name',)
    ordering = ('price',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'num_people', 'tariff', 'meal_option', 'is_confirmed', 'total_price', 'created')
    list_filter = ('is_confirmed', 'created', 'tour')
    search_fields = ('user__username', 'tour__hotel')
    ordering = ('-created',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tour', 'rating', 'date', 'text')
    list_filter = ('rating', 'date', 'tour')
    search_fields = ('user__username', 'tour__hotel', 'text')
    ordering = ('-date',)
