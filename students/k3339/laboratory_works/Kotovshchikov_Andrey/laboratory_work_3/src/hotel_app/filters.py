from django.utils import timezone
from django.db.models import Exists
from rest_framework.filters import BaseFilterBackend
from django_filters.rest_framework import filters, FilterSet

from hotel_app.models import Booking, Employee, Schedule


class IsRoomAvailableFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        available_param = request.query_params.get("available")
        if (available_param is None) or available_param.lower() != "true":
            return queryset

        return queryset.filter(
            ~Exists(
                Booking.objects.filter(
                    check_in_date__lte=timezone.now(),
                    check_out_date__gt=timezone.now(),
                )
            )
        )


class EmployeeFilter(FilterSet):
    guest_id = filters.NumberFilter(
        field_name="schedule__floor__rooms__booking__guest__id"
    )

    week_day = filters.ChoiceFilter(
        choices=Schedule.week_days,
        field_name="schedule__week_day",
    )

    class Meta:
        model = Employee
        fields = ("guest_id", "week_day")
