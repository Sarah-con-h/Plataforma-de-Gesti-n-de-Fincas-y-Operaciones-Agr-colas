from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trabajador, Asignacion
from .serializer import TrabajadorSerializer, AsignacionSerializer


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


class AsignacionViewSet(viewsets.ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['trabajador__nombres', 'tarea__titulo']
    ordering_fields = ['fecha_asignacion', 'completada']