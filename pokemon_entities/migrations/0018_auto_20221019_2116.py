# Generated by Django 3.1.14 on 2022-10-19 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0017_auto_20221019_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
