from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import Pokemon_search
import requests
from .models import User, Pokemon, db
from flask_login import login_required, current_user

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
@login_required
def poke_search():
    form = Pokemon_search()
    if request.method == "POST":
        pokemon_name = form.pokemon_name.data
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
        response = requests.get(url)
        if not response.ok:
                return 'Pokemon does not exist'
                
                

        data = response.json()
        for pokemon in data:
            poke_dict={
                    "id": data['id'],
                    "name": data['name'].title(),
                    #"type": data['type']['name'],
                    "ability":data['abilities'][0]["ability"]["name"],
                    "photo":data['sprites']['other']['home']["front_default"],
                    "attack": data['stats'][1]['base_stat'],
                    "hp":data['stats'][0]['base_stat'],
                    "defense":data['stats'][2]["base_stat"]}
            if not Pokemon.known_pokemon(poke_dict['name']):
                 pokemon = Pokemon()
                 pokemon.from_dict(poke_dict)
                 pokemon.saveToDB()
        return render_template('search.html', form = form, pokemon = poke_dict)
    return render_template('search.html', form = form)

@app.route('/catch/<id>')
@login_required
def catch_pokemon(id):
    pokemon = Pokemon.query.filter_by(id = id).first()
    if pokemon in current_user.pokemon:
        flash('Pokemon already in team!', 'warning')
        return redirect(url_for('poke_search'))
    elif current_user.pokemon.count() == 5:
        flash('Team is full please remove a pokemon to add another!', 'warning')
        return render_template('team.html', pokemon = pokemon)
    else:
        flash('Added to your team!', 'success')
        current_user.pokemon.append(pokemon)
        db.session.commit()
        return render_template('team.html', pokemon = pokemon)

         
@app.route('/team')
@login_required
def team():
     
    return render_template('team.html', team = current_user.pokemon.all())

# @app.route('edit')
# @login_required
# def edit_profile():
#     pass
