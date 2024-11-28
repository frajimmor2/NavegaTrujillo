import django_filters
from business.models import Ship

class ship_filter(django_filters.FilterSet):
    
    rent_per_day__lte = django_filters.NumberFilter(field_name='rent_per_day', lookup_expr='lte')
    capacity__gte = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    need_license_f = django_filters.BooleanFilter(field_name='need_license', lookup_expr='exact')

    class Meta:
        model = Ship
        fields = ['rent_per_day', 'capacity', 'need_license']