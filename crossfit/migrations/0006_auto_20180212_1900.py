# Generated by Django 2.0 on 2018-02-12 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crossfit', '0005_perfil_fechanacimiento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tener',
            name='actividad',
        ),
        migrations.RemoveField(
            model_name='tener',
            name='clase',
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='clase',
        ),
        migrations.AddField(
            model_name='horario',
            name='actividad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crossfit.Actividad'),
        ),
        migrations.AlterField(
            model_name='horario',
            name='clase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crossfit.Clase'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefono',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.DeleteModel(
            name='Tener',
        ),
    ]
