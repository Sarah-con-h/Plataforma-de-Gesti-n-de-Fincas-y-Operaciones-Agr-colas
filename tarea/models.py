from django.db import models
from django.core.validators import MinValueValidator
from fincas.models import Lote


class TipoTarea(models.Model):
    """Catálogo de tipos de tareas agrícolas"""
    
    CATEGORIA_CHOICES = [
        ('preparacion', 'Preparación del Terreno'),
        ('siembra', 'Siembra'),
        ('mantenimiento', 'Mantenimiento'),
        ('fertilizacion', 'Fertilización'),
        ('control_plagas', 'Control de Plagas'),
        ('riego', 'Riego'),
        ('poda', 'Poda'),
        ('cosecha', 'Cosecha'),
        ('postcosecha', 'Postcosecha'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    duracion_estimada_horas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Duración estimada en horas"
    )
    requiere_maquinaria = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Tipo de Tarea'
        verbose_name_plural = 'Tipos de Tareas'
    
    def _str_(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


class Tarea(models.Model):
    """Modelo para representar tareas agrícolas"""
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('pausada', 'Pausada'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    lote = models.ForeignKey(
        Lote,
        on_delete=models.CASCADE,
        related_name='tareas'
    )
    tipo_tarea = models.ForeignKey(
        TipoTarea,
        on_delete=models.PROTECT,
        related_name='tareas'
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_programada = models.DateField()
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDAD_CHOICES,
        default='media'
    )
    horas_estimadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)]
    )
    horas_reales = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    costo_estimado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    costo_real = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_programada', 'prioridad']
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        indexes = [
            models.Index(fields=['fecha_programada', 'estado']),
            models.Index(fields=['lote', 'estado']),
        ]
    
    def _str_(self):
        return f"{self.titulo} - {self.lote.codigo} ({self.get_estado_display()})"
    
    def total_trabajadores(self):
        """Retorna el número de trabajadores asignados"""
        return self.asignaciones.count()
    
    def total_insumos(self):
        """Retorna el número de insumos utilizados"""
        return self.consumos.count()
    
    def eficiencia_tiempo(self):
        """Calcula la eficiencia en tiempo (% horas reales vs estimadas)"""
        if self.horas_reales and self.horas_estimadas:
            return round((self.horas_estimadas / self.horas_reales) * 100, 2)
        return None
    
    def eficiencia_costo(self):
        """Calcula la eficiencia en costo (% costo real vs estimado)"""
        if self.costo_real and self.costo_estimado:
            return round((self.costo_estimado / self.costo_real) * 100, 2)
        return None