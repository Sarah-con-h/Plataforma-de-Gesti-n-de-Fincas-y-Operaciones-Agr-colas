from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Trabajador, Asignacion
from .serializer import TrabajadorSerializer, AsignacionSerializer


@extend_schema_view(
    list=extend_schema(tags=['👥 Trabajadores']),
    create=extend_schema(tags=['👥 Trabajadores']),
    retrieve=extend_schema(tags=['👥 Trabajadores']),
    update=extend_schema(tags=['👥 Trabajadores']),
    partial_update=extend_schema(tags=['👥 Trabajadores']),
    destroy=extend_schema(tags=['👥 Trabajadores']),
)
class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.all()
    serializer_class = TrabajadorSerializer

    # 2 filtros obligatorios
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombres', 'apellidos']
    ordering_fields = ['fecha_ingreso']

    # ENDPOINT EXTRA: trabajadores por rol
    @action(detail=False, methods=['get'], url_path="por-rol/(?P<rol>[^/.]+)")
    def trabajadores_por_rol(self, request, rol=None):
        trabajadores = Trabajador.objects.filter(rol=rol, activo=True)
        serializer = self.get_serializer(trabajadores, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=['👥 Asignaciones']),
    create=extend_schema(tags=['👥 Asignaciones']),
    retrieve=extend_schema(tags=['👥 Asignaciones']),
    update=extend_schema(tags=['👥 Asignaciones']),
    partial_update=extend_schema(tags=['👥 Asignaciones']),
    destroy=extend_schema(tags=['👥 Asignaciones']),
)
class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['trabajador__nombres', 'tarea__titulo']
    ordering_fields = ['fecha_asignacion', 'completada']