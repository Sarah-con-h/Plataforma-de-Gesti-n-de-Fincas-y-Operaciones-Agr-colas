from django.db import models
from django.core.validators import MinValueValidator


class Finca(models.Model):
    """Modelo para representar una finca o propiedad agrícola"""
    
    nombre = models.CharField(max_length=200, unique=True)
    ubicacion = models.CharField(max_length=500, help_text="Dirección o coordenadas")
    area_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Área total en hectáreas"
    )
    latitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Latitud (georreferenciación)"
    )
    longitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Longitud (georreferenciación)"
    )
    propietario = models.CharField(max_length=200)
    fecha_registro = models.DateField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = 'Finca'
        verbose_name_plural = 'Fincas'
    
    def __str__(self):
        return f"{self.nombre} - {self.area_total} ha"
    
    def total_lotes(self):
        """Retorna el número total de lotes en la finca"""
        return self.lotes.count()
    
    def area_cultivada(self):
        """Retorna el área total cultivada (suma de lotes)"""
        return self.lotes.aggregate(total=models.Sum('area'))['total'] or 0


class Lote(models.Model):
    """Modelo para representar un lote o parcela dentro de una finca"""
    
    ESTADO_CHOICES = [
        ('preparacion', 'En Preparación'),
        ('sembrado', 'Sembrado'),
        ('crecimiento', 'En Crecimiento'),
        ('cosecha', 'Listo para Cosecha'),
        ('barbecho', 'En Barbecho'),
        ('inactivo', 'Inactivo'),
    ]
    
    finca = models.ForeignKey(
        Finca, 
        on_delete=models.CASCADE, 
        related_name='lotes'
    )
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    area = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Área del lote en hectáreas"
    )
    cultivo_actual = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Cultivo actual del lote"
    )
    fecha_siembra = models.DateField(null=True, blank=True)
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='preparacion'
    )
    coordenadas_poligono = models.TextField(
        blank=True,
        help_text="Coordenadas del polígono en formato JSON"
    )
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['finca', 'codigo']
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
    
    def __str__(self):
        return f"{self.codigo} - {self.finca.nombre}"
    
    def dias_desde_siembra(self):
        """Retorna los días transcurridos desde la siembra"""
        if self.fecha_siembra:
            from django.utils import timezone
            return (timezone.now().date() - self.fecha_siembra).days
        return None
    
    def tareas_pendientes(self):
        """Retorna el número de tareas pendientes en este lote"""
        return self.tareas.filter(estado='pendiente').count()