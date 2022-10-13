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
    longitude = models.FloatField('lat')
    latitude = models.FloatField('lon')
