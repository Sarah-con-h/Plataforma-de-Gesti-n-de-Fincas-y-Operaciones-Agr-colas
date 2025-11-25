from django.contrib import admin
from .models import Trabajador, Asignacion

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('numero_identificacion', 'nombres', 'apellidos', 'rol', 'activo')
    search_fields = ('numero_identificacion', 'nombres', 'apellidos')
    list_filter = ('rol', 'activo', 'tipo_contrato')

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'tarea', 'fecha_asignacion', 'horas_asignadas', 'completada')
    search_fields = ('trabajador__nombres', 'trabajador__apellidos', 'tarea__titulo')
    list_filter = ('completada',)