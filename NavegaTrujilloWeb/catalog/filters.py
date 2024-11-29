import django_filters
from business.models import Ship
from django import forms

class ship_filter(django_filters.FilterSet):
    
    rent_per_day__lte = django_filters.NumberFilter(field_name='rent_per_day', lookup_expr='lte', label='Coste diario (máximo)')
    capacity__gte = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte', label= 'Capacidad (mínima)')
    need_license_f = django_filters.BooleanFilter(field_name='need_license', lookup_expr='exact', label='Necesita licencia')
    

    class Meta:
        model = Ship
        fields = []

    