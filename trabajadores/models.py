

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from tareas.models import Tarea


class Trabajador(models.Model):
    """Modelo para representar trabajadores de la finca"""
    
    ROL_CHOICES = [
        ('operario', 'Operario'),
        ('tecnico', 'Técnico Agrícola'),
        ('supervisor', 'Supervisor'),
        ('maquinista', 'Operador de Maquinaria'),
        ('especialista', 'Especialista'),
        ('jefe_campo', 'Jefe de Campo'),
    ]
    
    TIPO_CONTRATO_CHOICES = [
        ('indefinido', 'Indefinido'),
        ('temporal', 'Temporal'),
        ('por_obra', 'Por Obra'),
        ('jornalero', 'Jornalero'),
    ]
    
    # Información personal
    numero_identificacion = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[0-9]+$',
                message='El número de identificación solo debe contener dígitos'
            )
        ]
    )
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    
    # Información laboral
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    tipo_contrato = models.CharField(
        max_length=20,
        choices=TIPO_CONTRATO_CHOICES,
        default='temporal'
    )
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    # Información salarial
    salario_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Salario base mensual"
    )
    valor_hora = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Valor por hora trabajada"
    )
    
    # Habilidades y certificaciones
    especialidades = models.TextField(
        blank=True,
        help_text="Especialidades o habilidades especiales"
    )
    certificaciones = models.TextField(
        blank=True,
        help_text="Certificaciones profesionales"
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['apellidos', 'nombres']
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
        indexes = [
            models.Index(fields=['rol', 'activo']),
            models.Index(fields=['numero_identificacion']),
        ]
    
    def _str_(self):
        return f"{self.nombres} {self.apellidos} - {self.get_rol_display()}"
    
    def nombre_completo(self):
        """Retorna el nombre completo del trabajador"""
        return f"{self.nombres} {self.apellidos}"
    
    def edad(self):
        """Calcula la edad del trabajador"""
        from django.utils import timezone
        hoy = timezone.now().date()
        edad = hoy.year - self.fecha_nacimiento.year
        if hoy.month < self.fecha_nacimiento.month or \
           (hoy.month == self.fecha_nacimiento.month and hoy.day < self.fecha_nacimiento.day):
            edad -= 1
        return edad
    
    def anos_servicio(self):
        """Calcula los años de servicio"""
        from django.utils import timezone
        fecha_fin = self.fecha_salida or timezone.now().date()
        anos = fecha_fin.year - self.fecha_ingreso.year
        if fecha_fin.month < self.fecha_ingreso.month or \
           (fecha_fin.month == self.fecha_ingreso.month and fecha_fin.day < self.fecha_ingreso.day):
            anos -= 1
        return anos
    
    def total_asignaciones(self):
        """Retorna el total de asignaciones del trabajador"""
        return self.asignaciones.count()


class Asignacion(models.Model):
    """Modelo para representar la asignación de trabajadores a tareas"""
    
    trabajador = models.ForeignKey(
        Trabajador,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name='asignaciones'
    )
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    horas_asignadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
        help_text="Horas asignadas para esta tarea"
    )
    horas_trabajadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Horas realmente trabajadas"
    )
    rol_en_tarea = models.CharField(
        max_length=100,
        blank=True,
        help_text="Rol específico en esta tarea"
    )
    observaciones = models.TextField(blank=True)
    completada = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_asignacion']
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'
        unique_together = ['trabajador', 'tarea']
        indexes = [
            models.Index(fields=['trabajador', 'completada']),
            models.Index(fields=['tarea', 'fecha_asignacion']),
        ]
    
    def _str_(self):
        return f"{self.trabajador.nombre_completo()} → {self.tarea.titulo}"
    
    def costo_mano_obra(self):
        """Calcula el costo de mano de obra basado en horas trabajadas"""
        if self.horas_trabajadas:
            return self.horas_trabajadas * self.trabajador.valor_hora
        return self.horas_asignadas * self.trabajador.valor_hora
    
    def eficiencia(self):
        """Calcula la eficiencia (% horas trabajadas vs asignadas)"""
        if self.horas_trabajadas and self.horas_asignadas:
            return round((self.horas_asignadas / self.horas_trabajadas) * 100, 2)
        return None