# Generated by Django 2.0 on 2018-02-13 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossfit', '0007_auto_20180213_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservar',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
