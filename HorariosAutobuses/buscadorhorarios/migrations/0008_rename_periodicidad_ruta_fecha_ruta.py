# Generated by Django 4.1.2 on 2022-11-22 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buscadorhorarios', '0007_alter_ruta_raw_json_data_alter_ruta_slug_vuelta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ruta',
            old_name='periodicidad',
            new_name='fecha_ruta',
        ),
    ]