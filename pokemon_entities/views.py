import folium  # type: ignore
from django.http import HttpResponseNotFound

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons = Pokemon.objects.all()
    local_time = localtime()
    pokemons_entity = PokemonEntity.objects.filter(
        appeared_at__lt=local_time,
        disappeared_at__gt=local_time,
    )

    for pokemon_entity in pokemons_entity:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            image_url=request.build_absolute_uri(
                pokemon_entity.pokemon.photo.url
            )
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title_ru,
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = Pokemon.objects.filter(id=pokemon_id).first()
    pokemon_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url,
        'title_ru': pokemon.title_ru,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'previous_evolution': None,
        'next_evolution': None,
        'entities': True
    }

    if not pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    local_time = localtime()
    pokemon_entities = pokemon.entities.filter(
        appeared_at__lt=local_time,
        disappeared_at__gt=local_time
    )
    if not pokemon_entities:
        pokemon_on_page['entities'] = None
        return render(request, 'pokemon.html', context={
            'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
        })

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            image_url=request.build_absolute_uri(
                pokemon_entity.pokemon.photo.url
            )
        )

    if pokemon.previous_evolution:
        previous_evolution_pokemon = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title_ru,
            'img_url': pokemon.previous_evolution.photo.url,
        }
        pokemon_on_page['previous_evolution'] = previous_evolution_pokemon

    pokemon_next_evolution = pokemon.next_evolutions.first()
    if pokemon_next_evolution:
        next_evolution_pokemon = {
            'pokemon_id': pokemon_next_evolution.id,
            'title_ru': pokemon_next_evolution.title_ru,
            'img_url': pokemon_next_evolution.photo.url,
        }
        pokemon_on_page['next_evolution'] = next_evolution_pokemon

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
