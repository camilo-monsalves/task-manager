from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarea(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso','En Progreso'),
        ('completada','Completada')
    )

    CATEGORIA_CHOICES = (
        ('trabajo','Trabajo'),
        ('hogar','Hogar'),
        ('estudio', 'Estudio')
    )

    PRIORIDAD_CHOICES = (
        ('prioridad_alta', 'Prioridad Alta'),
        ('prioridad_media', 'Prioridad Media'),
        ('baja_prioridad', 'Prioridad Baja')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tareas_creadas')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    observacion = models.TextField(null=True)
    asignado_a = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas')
    asignado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_asignadas_por')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='prioridad_media')

    def __str__(self):
        return self.titulo
    