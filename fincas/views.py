from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Finca, Lote
from .serializers import FincaSerializer, FincaListSerializer, LoteSerializer


@extend_schema_view(
    list=extend_schema(tags=['🏠 Gestión de Fincas']),
    create=extend_schema(tags=['🏠 Gestión de Fincas']),
    retrieve=extend_schema(tags=['🏠 Gestión de Fincas']),
    update=extend_schema(tags=['🏠 Gestión de Fincas']),
    partial_update=extend_schema(tags=['🏠 Gestión de Fincas']),
    destroy=extend_schema(tags=['🏠 Gestión de Fincas']),
)
class FincaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Fincas.
    
    Proporciona operaciones CRUD completas para fincas:
    - GET /api/fincas/ - Listar todas las fincas
    - POST /api/fincas/ - Crear una nueva finca
    - GET /api/fincas/{id}/ - Obtener detalles de una finca
    - PUT /api/fincas/{id}/ - Actualizar una finca
    - DELETE /api/fincas/{id}/ - Eliminar una finca
    """
    queryset = Finca.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'propietario', 'ubicacion']
    ordering_fields = ['nombre', 'fecha_registro', 'area_total']
    ordering = ['nombre']
    
    def get_serializer_class(self):
        """Usa serializer simplificado para listar, completo para detalle"""
        if self.action == 'list':
            return FincaListSerializer
        return FincaSerializer
    
    @action(detail=True, methods=['get'])
    def lotes(self, request, pk=None):
        """Obtener todos los lotes de una finca específica"""
        finca = self.get_object()
        lotes = finca.lotes.all()
        serializer = LoteSerializer(lotes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas de una finca"""
        finca = self.get_object()
        return Response({
            'nombre': finca.nombre,
            'area_total': str(finca.area_total),
            'total_lotes': finca.total_lotes(),
            'area_cultivada': str(finca.area_cultivada()),
        })


@extend_schema_view(
    list=extend_schema(tags=['🏠 Gestión de Lotes']),
    create=extend_schema(tags=['🏠 Gestión de Lotes']),
    retrieve=extend_schema(tags=['🏠 Gestión de Lotes']),
    update=extend_schema(tags=['🏠 Gestión de Lotes']),
    partial_update=extend_schema(tags=['🏠 Gestión de Lotes']),
    destroy=extend_schema(tags=['🏠 Gestión de Lotes']),
)
class LoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar Lotes.
    
    Proporciona operaciones CRUD completas para lotes:
    - GET /api/lotes/ - Listar todos los lotes
    - POST /api/lotes/ - Crear un nuevo lote
    - GET /api/lotes/{id}/ - Obtener detalles de un lote
    - PUT /api/lotes/{id}/ - Actualizar un lote
    - DELETE /api/lotes/{id}/ - Eliminar un lote
    """
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'codigo', 'cultivo_actual', 'finca__nombre']
    ordering_fields = ['codigo', 'fecha_creacion', 'estado']
    ordering = ['finca', 'codigo']
    
    @action(detail=True, methods=['get'])
    def tareas_pendientes(self, request, pk=None):
        """Obtener número de tareas pendientes en el lote"""
        lote = self.get_object()
        return Response({
            'lote': lote.codigo,
            'tareas_pendientes': lote.tareas_pendientes(),
        })
    
    @action(detail=True, methods=['get'])
    def dias_desde_siembra(self, request, pk=None):
        """Obtener días transcurridos desde la siembra"""
        lote = self.get_object()
        dias = lote.dias_desde_siembra()
        return Response({
            'lote': lote.codigo,
            'fecha_siembra': lote.fecha_siembra,
            'dias_desde_siembra': dias,
        })
