from django.db import models  # type: ignore
from django.utils.timezone import localtime


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    title_en = models.CharField(verbose_name='Название на Английском', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название на Японском', max_length=200, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolutions',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    photo = models.ImageField(
        upload_to='pokemon_images',
        verbose_name='Фото покемона'
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='pokemon_entities'
    )
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    appeared_at = models.DateTimeField(null=True, verbose_name='Время появления покемона')
    disappeared_at = models.DateTimeField(null=True, verbose_name='Время исчезновения покемона')

    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stigma = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)

    def __str__(self):
        is_vision = self.appeared_at < localtime() < self.disappeared_at
        return f'{self.pokemon.title} {f"Покемон виден" if is_vision else "Покемона нет"}'
