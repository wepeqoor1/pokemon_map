# Generated by Django 3.1.14 on 2022-10-19 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0020_pokemon_is_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='is_delete',
        ),
    ]
