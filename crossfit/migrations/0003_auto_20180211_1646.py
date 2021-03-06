# Generated by Django 2.0 on 2018-02-11 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crossfit', '0002_auto_20180211_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50, unique=True)),
                ('aforo', models.PositiveSmallIntegerField(default=6)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diaSemana', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], default='Lunes', max_length=12)),
                ('horaInicio', models.CharField(max_length=12)),
                ('horaFin', models.CharField(max_length=12)),
                ('clase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crossfit.Clase')),
            ],
        ),
        migrations.CreateModel(
            name='Tener',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crossfit.Actividad')),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crossfit.Clase')),
            ],
        ),
        migrations.AddField(
            model_name='actividad',
            name='clase',
            field=models.ManyToManyField(through='crossfit.Tener', to='crossfit.Clase'),
        ),
    ]
