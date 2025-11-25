import django_filters
from .models import Insumo, Movimiento, Consumo

class InsumoFilter(django_filters.FilterSet):
    categoria = django_filters.CharFilter(lookup_expr='icontains')
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Insumo
        fields = ['categoria', 'nombre', 'proveedor']


class MovimientoFilter(django_filters.FilterSet):
    fecha = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Movimiento
        fields = ['tipo', 'fecha']


class ConsumoFilter(django_filters.FilterSet):
    fecha_consumo = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Consumo
        fields = ['insumo', 'tarea']