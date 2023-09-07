# Generated by Django 4.2.4 on 2023-09-05 23:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0003_tarea_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='asignado_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tareas_asignadas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas_creadas', to=settings.AUTH_USER_MODEL),
        ),
    ]
