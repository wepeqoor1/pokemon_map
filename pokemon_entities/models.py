from django.db import models  # type: ignore


class Pokemon(models.Model):
    title = models.CharField('Название', max_length=200)
    title_en = models.CharField('Название на Английском', max_length=200)
    title_jp = models.CharField('Название на Японском', max_length=200)
    previous_evolution = models.ForeignKey(
        'self',
        related_name='next_evolution',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    photo = models.ImageField(
        upload_to='pokemon_images',
        null=True,
        blank=True
    )
    description = models.TextField('Описание', default='Описание покемона')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
    )
    latitude = models.FloatField('lat')
    longitude = models.FloatField('lon')

    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)

    level = models.IntegerField(blank=True)
    health = models.IntegerField(blank=True)
    strength = models.IntegerField(blank=True)
    defence = models.IntegerField(blank=True)
    stigma = models.IntegerField(blank=True)

    def __str__(self):
        return self.pokemon.title
