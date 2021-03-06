# Generated by Django 2.0 on 2018-02-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossfit', '0018_oficial_categoria'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entreno',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterModelOptions(
            name='oficial',
            options={'ordering': ['nombre']},
        ),
        migrations.AlterField(
            model_name='entreno',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='oficial',
            name='nombre',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
