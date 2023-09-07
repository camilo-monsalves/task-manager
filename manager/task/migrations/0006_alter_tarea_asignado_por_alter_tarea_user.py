# Generated by Django 4.2.4 on 2023-09-06 23:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0005_tarea_asignado_por'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='asignado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_asignadas_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tareas_creadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
