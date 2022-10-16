import folium  # type: ignore

from django.shortcuts import render, get_list_or_404
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
    pokemons_entity = get_list_or_404(
        PokemonEntity,
        appeared_at__lt=localtime(),
        disappeared_at__gt=localtime(),
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

    pokemons = get_list_or_404(Pokemon)
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = get_list_or_404(
        PokemonEntity,
        pokemon_id=pokemon_id,
        appeared_at__lt=localtime(),
        disappeared_at__gt=localtime()
    )

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map=folium_map,
            lat=pokemon_entity.latitude,
            lon=pokemon_entity.longitude,
            image_url=request.build_absolute_uri(
                pokemon_entity.pokemon.photo.url
            )
        )
    pokemon = Pokemon.objects.get(id=int(pokemon_id))
    pokemon_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': pokemon.photo.url,
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'previous_evolution': None
    }
    previous_evolution = Pokemon.objects.filter(id=pokemon.previous_evolution_id).first()
    if previous_evolution:
        previous_evolution = {
            'pokemon_id': previous_evolution.id,
            'title_ru': previous_evolution.title,
            'img_url': previous_evolution.photo.url,
        }
        pokemon_on_page['previous_evolution'] = previous_evolution

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
