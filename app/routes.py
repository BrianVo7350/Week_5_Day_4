from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import Pokemon_search
import requests
from .models import User
from flask_login import login_required

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def poke_search():
    form = Pokemon_search()
    if request.method == "POST":
        pokemon_name = form.pokemon_name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
        response = requests.get(url)
        if not response.ok:
                return "Try again?"

        data = response.json()
        for pokemon in data:
            poke_dict={
                    "poke_id": data['id'],
                    "name": data['name'].title(),
                    "type": data['type']['name'],
                    "ability":data['abilities'][0]["ability"]["name"],
                    "base experience":data['base_experience'],
                    "photo":data['sprites']['other']['home']["front_default"],
                    "attack": data['stats'][1]['base_stat'],
                    "hp":data['stats'][0]['base_stat'],
                    "defense":data['stats'][2]["base_stat"]}
            pokemon = poke_dict
        return render_template('search.html', form = form, pokemon = pokemon)
        #pokemon.saveToDB()
    return render_template('search.html', form = form)

