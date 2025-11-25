from django.contrib import admin
from .models import Insumo, Movimiento, Consumo

admin.site.register(Insumo)
admin.site.register(Movimiento)
admin.site.register(Consumo)