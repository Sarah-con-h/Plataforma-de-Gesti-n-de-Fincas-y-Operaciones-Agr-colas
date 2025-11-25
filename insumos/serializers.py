from rest_framework import serializers
from .models import Insumo, Movimiento, Consumo

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = '__all__'


class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'

    def validate(self, data):
        insumo = data["insumo"]
        tipo = data["tipo"]
        cantidad = data["cantidad"]

        if tipo == "salida" and cantidad > insumo.stock_actual:
            raise serializers.ValidationError(
                "No hay suficiente stock disponible para realizar la salida."
            )
        return data


class ConsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumo
        fields = '__all__'