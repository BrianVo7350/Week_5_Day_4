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
    elif current_user.pokemon.count() == 6:
        flash('Team is full please remove a pokemon to add another!', 'warning')
        return render_template('team.html', pokemon = pokemon, user = current_user)
    else:
        flash('Added to your team!', 'success')
        current_user.pokemon.append(pokemon)
        db.session.commit()
        return render_template('team.html', pokemon = pokemon, user = current_user)

         
@app.route('/team')
@login_required
def team():
    return render_template('team.html', team = current_user.pokemon.all(), user = current_user)

@app.route('/opteam/<id>')
@login_required
def opteam(id):
    user = User.query.filter_by(id = id).first()
    return render_template('team.html', team = user.pokemon.all(), user = user)

@app.route('/showuser')
@login_required
def show_users():
    users = User.query.filter(User.id != current_user.id, User.pokemon).all()
    return render_template('allusers.html', users = users)




@app.route('/battle/<id>')
@login_required
def battle(id):
    wins = 0 
    losses = 0

    user = User.query.get(id)
    current_team = current_user.pokemon
    op_team = user.pokemon
    current_total = 0
    op_total = 0

    for pokemon in op_team:
        op_total += pokemon.attack
        op_total += pokemon.defense
        op_total += pokemon.hp

    for pokemon in current_team:
        current_total += pokemon.attack
        current_total += pokemon.defense
        current_total += pokemon.hp

    if op_total > current_total:
        user.addwin()
        current_user.addloss()
        flash('Lost Match!')
    elif op_total < current_total:
        current_user.addwin()
        user.addloss()
        flash('Won Match!')
    else:
        flash('Both Trainers Down Draw!')

    return render_template('team.html', wins=wins, losses=losses, user=user)

