from rest_framework import serializers
from .models import TipoTarea, Tarea

class TipoTareaSerializer(serializers.ModelSerializer):

    # VALIDACIÓN PERSONALIZADA
    def validate_duracion_estimada_horas(self, value):
        if value <= 0:
            raise serializers.ValidationError("La duración estimada debe ser mayor a 0.")
        return value

    class Meta:
        model = TipoTarea
        fields = '__all__'


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'
