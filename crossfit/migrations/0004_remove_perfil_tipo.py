# Generated by Django 2.0 on 2018-02-11 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crossfit', '0003_auto_20180211_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='tipo',
        ),
    ]
