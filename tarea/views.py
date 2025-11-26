from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import TipoTarea, Tarea
from .serializer import TipoTareaSerializer, TareaSerializer


@extend_schema_view(
    list=extend_schema(tags=['🌾 Tipos de Tarea']),
    create=extend_schema(tags=['🌾 Tipos de Tarea']),
    retrieve=extend_schema(tags=['🌾 Tipos de Tarea']),
    update=extend_schema(tags=['🌾 Tipos de Tarea']),
    partial_update=extend_schema(tags=['🌾 Tipos de Tarea']),
    destroy=extend_schema(tags=['🌾 Tipos de Tarea']),
)
class TipoTareaViewSet(viewsets.ModelViewSet):
    queryset = TipoTarea.objects.all()
    serializer_class = TipoTareaSerializer

    # 2 filtros obligatorios
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['categoria', 'nombre']
    ordering_fields = ['duracion_estimada_horas']


@extend_schema_view(
    list=extend_schema(tags=['🌾 Operaciones - Tareas']),
    create=extend_schema(tags=['🌾 Operaciones - Tareas']),
    retrieve=extend_schema(tags=['🌾 Operaciones - Tareas']),
    update=extend_schema(tags=['🌾 Operaciones - Tareas']),
    partial_update=extend_schema(tags=['🌾 Operaciones - Tareas']),
    destroy=extend_schema(tags=['🌾 Operaciones - Tareas']),
)
class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

    # 2 filtros obligatorios
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['estado', 'tipo_tarea__nombre']
    ordering_fields = ['fecha']

    # ENDPOINT EXTRA OBLIGATORIO
    @action(detail=False, methods=['get'], url_path="por-lote/(?P<lote_id>[^/.]+)")
    def tareas_por_lote(self, request, lote_id=None):
        tareas = Tarea.objects.filter(lote_id=lote_id)
        serializer = self.get_serializer(tareas, many=True)
        return Response(serializer.data)
