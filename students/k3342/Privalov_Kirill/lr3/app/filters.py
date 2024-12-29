import django_filters
from .models import LaborContract, Schedule

class ScheduleFilter(django_filters.FilterSet):
    doctorId = django_filters.NumberFilter(field_name='doctor__doctorId', lookup_expr='exact')

    class Meta:
        model = Schedule
        fields = ['doctorId']

class LaborContractFilter(django_filters.FilterSet):
    doctorId = django_filters.NumberFilter(field_name='doctor__doctorId', lookup_expr='exact')

    class Meta:
        model = LaborContract
        fields = ['doctorId']