from django.db import models
from django.core.validators import MinValueValidator
from tarea.models import Tarea


class Insumo(models.Model):
    """Modelo para representar insumos agrícolas"""
    
    CATEGORIA_CHOICES = [
        ('fertilizante', 'Fertilizante'),
        ('pesticida', 'Pesticida'),
        ('herbicida', 'Herbicida'),
        ('fungicida', 'Fungicida'),
        ('semilla', 'Semilla'),
        ('abono', 'Abono Orgánico'),
        ('combustible', 'Combustible'),
        ('herramienta', 'Herramienta'),
        ('otro', 'Otro'),
    ]
    
    UNIDAD_MEDIDA_CHOICES = [
        ('kg', 'Kilogramo'),
        ('g', 'Gramo'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('unidad', 'Unidad'),
        ('bulto', 'Bulto'),
        ('galon', 'Galón'),
        ('tonelada', 'Tonelada'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(
        max_length=20,
        choices=UNIDAD_MEDIDA_CHOICES,
        default='kg'
    )
    
    # Inventario
    stock_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    stock_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Nivel mínimo de stock para alerta"
    )
    stock_maximo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Información de costos
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Precio por unidad de medida"
    )
    
    # Información adicional
    proveedor = models.CharField(max_length=200, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    lote_proveedor = models.CharField(max_length=100, blank=True)
    
    # Seguridad y medio ambiente
    requiere_receta = models.BooleanField(
        default=False,
        help_text="Requiere receta o autorización especial"
    )
    toxico = models.BooleanField(default=False)
    periodo_carencia = models.IntegerField(
        null=True,
        blank=True,
        help_text="Días de carencia antes de cosecha"
    )
    
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['categoria', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def stock_bajo(self):
        """Verifica si el stock está por debajo del mínimo"""
        return self.stock_actual < self.stock_minimo
    
    def valor_inventario(self):
        """Calcula el valor total del inventario actual"""
        return self.stock_actual * self.precio_unitario
    
    def consumo_total(self):
        """Retorna el consumo total del insumo"""
        return self.consumos.aggregate(
            total=models.Sum('cantidad')
        )['total'] or 0


class Movimiento(models.Model):
    """Modelo para registrar movimientos de inventario (entradas/salidas)"""
    
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('merma', 'Merma'),
        ('devolucion', 'Devolución'),
    ]
    
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    documento_referencia = models.CharField(
        max_length=100,
        blank=True,
        help_text="Número de factura, orden de compra, etc."
    )
    costo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    responsable = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        indexes = [
            models.Index(fields=['insumo', 'tipo', 'fecha']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.insumo.nombre} - {self.cantidad} {self.insumo.unidad_medida}"
    
    def costo_total(self):
        """Calcula el costo total del movimiento"""
        if self.costo_unitario:
            return self.cantidad * self.costo_unitario
        return self.cantidad * self.insumo.precio_unitario


class Consumo(models.Model):
    """Modelo para registrar consumo de insumos en tareas"""
    
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        related_name='consumos'
    )
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name='consumos'
    )
    cantidad = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    fecha_consumo = models.DateTimeField(auto_now_add=True)
    aplicador = models.CharField(
        max_length=200,
        blank=True,
        help_text="Persona que aplicó el insumo"
    )
    dosis_aplicada = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ejemplo: 2L/ha, 50g/planta"
    )
    condiciones_clima = models.CharField(
        max_length=200,
        blank=True,
        help_text="Condiciones climáticas durante la aplicación"
    )
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_consumo']
        verbose_name = 'Consumo'
        verbose_name_plural = 'Consumos'
        indexes = [
            models.Index(fields=['insumo', 'tarea']),
            models.Index(fields=['fecha_consumo']),
        ]
    
    def __str__(self):
        return f"{self.insumo.nombre} - {self.tarea.titulo} ({self.cantidad} {self.insumo.unidad_medida})"
    
    def costo_consumo(self):
        """Calcula el costo del consumo"""
        return self.cantidad * self.insumo.precio_unitario