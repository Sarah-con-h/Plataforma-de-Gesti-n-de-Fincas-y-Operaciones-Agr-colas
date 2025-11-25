from rest_framework import serializers
from .models import Trabajador, Asignacion

class TrabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

class AsignacionSerializer(serializers.ModelSerializer):
    trabajador_nombres = serializers.CharField(source='trabajador.nombres', read_only=True)
    tarea_titulo = serializers.CharField(source='tarea.titulo', read_only=True)
    
    class Meta:
        model = Asignacion
        fields = '__all__'