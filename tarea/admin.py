from django.contrib import admin
from .models import TipoTarea, Tarea


@admin.register(TipoTarea)
class TipoTareaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'duracion_estimada_horas', 'activo']
    list_filter = ['categoria', 'activo']
    search_fields = ['nombre', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'lote', 'estado', 'prioridad', 'fecha_programada']
    list_filter = ['estado', 'prioridad', 'fecha_programada']
    search_fields = ['titulo', 'lote__codigo']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_programada'
    
    actions = ['marcar_completada', 'marcar_cancelada']
    
    def marcar_completada(self, request, queryset):
        queryset.update(estado='completada')
        self.message_user(request, f'{queryset.count()} tarea(s) completada(s)')
    marcar_completada.short_description = 'Marcar como Completadas'
    
    def marcar_cancelada(self, request, queryset):
        queryset.update(estado='cancelada')
        self.message_user(request, f'{queryset.count()} tarea(s) cancelada(s)')
    marcar_cancelada.short_description = 'Marcar como Canceladas'
