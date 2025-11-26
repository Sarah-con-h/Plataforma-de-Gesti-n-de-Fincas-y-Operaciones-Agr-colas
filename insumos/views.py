from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Insumo, Movimiento, Consumo
from .serializers import InsumoSerializer, MovimientoSerializer, ConsumoSerializer
from .filters import InsumoFilter, MovimientoFilter, ConsumoFilter


# ===== INSUMOS =====

@extend_schema(tags=['📦 Insumos'])
class InsumoListCreateView(generics.ListCreateAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = InsumoFilter


@extend_schema(tags=['📦 Insumos'])
class InsumoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Insumo.objects.all()
    serializer_class = InsumoSerializer


# ===== MOVIMIENTOS =====

@extend_schema(tags=['📦 Movimientos'])
class MovimientoListCreateView(generics.ListCreateAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovimientoFilter


@extend_schema(tags=['📦 Movimientos'])
class MovimientoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer


# ===== CONSUMOS =====

@extend_schema(tags=['📦 Consumos'])
class ConsumoListCreateView(generics.ListCreateAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsumoFilter


@extend_schema(tags=['📦 Consumos'])
class ConsumoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consumo.objects.all()
    serializer_class = ConsumoSerializer


# ===== ENDPOINT EXTRA =====

@api_view(['GET'])
@extend_schema(tags=['📦 Resumen Inventario'])
def resumen_inventario(request):
    total_insumos = Insumo.objects.count()
    valor_total = sum(i.valor_inventario() for i in Insumo.objects.all())
    insumos_bajo_stock = Insumo.objects.filter(stock_actual__lt=models.F('stock_minimo')).count()

    return Response({
        "total_insumos": total_insumos,
        "valor_total_inventario": valor_total,
        "insumos_bajo_stock": insumos_bajo_stock,
    })