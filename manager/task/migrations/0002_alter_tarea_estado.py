# Generated by Django 4.2.4 on 2023-08-30 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarea',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('en_progreso', 'En Progreso'), ('completada', 'Completada')], default='pendiente', max_length=20),
        ),
    ]
