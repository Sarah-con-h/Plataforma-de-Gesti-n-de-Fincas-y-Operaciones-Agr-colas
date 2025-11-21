from rest_framework import serializers
from .models import Finca, Lote


class LoteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Lote"""
    
    class Meta:
        model = Lote
        fields = [
            'id', 'finca', 'codigo', 'nombre', 'area', 'cultivo_actual',
            'fecha_siembra', 'estado', 'coordenadas_poligono', 'observaciones',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']


class FincaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Finca"""
    lotes = LoteSerializer(many=True, read_only=True)
    total_lotes = serializers.SerializerMethodField()
    area_cultivada = serializers.SerializerMethodField()
    
    class Meta:
        model = Finca
        fields = [
            'id', 'nombre', 'ubicacion', 'area_total', 'latitud', 'longitud',
            'propietario', 'fecha_registro', 'activa', 'lotes', 'total_lotes',
            'area_cultivada'
        ]
        read_only_fields = ['id', 'fecha_registro']
    
    def get_total_lotes(self, obj):
        return obj.total_lotes()
    
    def get_area_cultivada(self, obj):
        return obj.area_cultivada()


class FincaListSerializer(serializers.ModelSerializer):
    """Serializador simplificado para listar fincas"""
    total_lotes = serializers.SerializerMethodField()
    
    class Meta:
        model = Finca
        fields = [
            'id', 'nombre', 'ubicacion', 'area_total', 'propietario',
            'activa', 'total_lotes'
        ]
    
    def get_total_lotes(self, obj):
        return obj.total_lotes()
