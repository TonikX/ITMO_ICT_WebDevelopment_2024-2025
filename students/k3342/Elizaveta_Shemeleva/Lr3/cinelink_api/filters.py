import django_filters

from cinelink_api.models import Movie


class MovieFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = django_filters.NumberFilter(field_name="rating", lookup_expr="lte")
    genres = django_filters.CharFilter(field_name="genres", lookup_expr="icontains")
    year_range = django_filters.NumericRangeFilter(field_name="year")

    class Meta:
        model = Movie
        fields = {
            "genres": ["icontains"],  # Filter for genre (case-insensitive)
            "year": ["exact", "gte", "lte"],  # Year-based filtering
            "rating": ["exact", "gte", "lte"],  # Rating-based filtering
        }
