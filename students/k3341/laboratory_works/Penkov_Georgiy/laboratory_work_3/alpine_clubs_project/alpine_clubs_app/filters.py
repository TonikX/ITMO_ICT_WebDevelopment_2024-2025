from django_filters import rest_framework as filters
from .models import ClubMembership


class ClubMembershipFilter(filters.FilterSet):
    active = filters.BooleanFilter(field_name="leave_datetime", lookup_expr="isnull")

    class Meta:
        model = ClubMembership
        fields = ["active"]
