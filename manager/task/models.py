from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarea(models.Model):
    ESTADO_CHOICES = (
        ('pendiete', 'Pendiente'),
        ('en_progreso','En Progreso'),
        ('completada','Completada')
    )

    CATEGORIA_CHOICES = (
        ('trabajo','Trabajo'),
        ('hogar','Hogar'),
        ('estudio', 'Estudio')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return self.titulo
    