from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(
        upload_to='pokemon_images',
        null=True,
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
    )
    longitude = models.FloatField('lat')
    latitude = models.FloatField('lon')
    appeared_at = models.DateTimeField(blank=True, null=True)
    disappeared_at = models.DateTimeField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    defence = models.IntegerField(blank=True, null=True)
    stigma = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.pokemon.name
