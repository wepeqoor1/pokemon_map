# Generated by Django 4.1.2 on 2022-10-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20221013_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='description',
            field=models.TextField(default='Описание покемона'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='latitude',
            field=models.FloatField(verbose_name='lat'),
        ),
        migrations.AlterField(
            model_name='pokemonentity',
            name='longitude',
            field=models.FloatField(verbose_name='lon'),
        ),
    ]
