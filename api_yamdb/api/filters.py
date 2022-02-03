import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Custom filter for Title model."""
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']