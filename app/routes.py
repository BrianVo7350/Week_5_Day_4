from flask import render_template, request, flash, redirect, url_for
from app import app
from forms import Pokemon_search, Signup, Login
import requests
from .models import User
from flask_login import login_user, logout_user, login_required

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/signup', methods = ["POST", "GET"])
def signup():
    form = Signup()
    if request.method == 'POST':
        if form.validate():
              username = form.username.data
              email = form.email.data
              password = form.password.data

              user = User(username, email, password)

              user.saveToDB()
              account = {
                   'username' : username,
                   'email' : email
              }
        return render_template('signup.html', form = form, account = account)
    return render_template('signup.html', form = form)

@app.route('/login', methods = ["POST", "GET"])
def login_page():
    form = Login()
    if request.method == 'POST':
         if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username = username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    print('invalid password')
            else:
                print('incorrect username or password')

            return render_template('login.html', form = form)
    return render_template('login.html', form = form)
         
 
@app.route('/logout')
def logMeOut():
    logout_user()
    return redirect(url_for('login.html'))

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
            poke_dict={}
            poke_dict={
                    "poke_id": data['id'],
                    "name": data['name'].title(),
                    "ability":data['abilities'][0]["ability"]["name"],
                    "base experience":data['base_experience'],
                    "photo":data['sprites']['other']['home']["front_default"],
                    "attack base stat": data['stats'][1]['base_stat'],
                    "hp base stat":data['stats'][0]['base_stat'],
                    "defense stat":data['stats'][2]["base_stat"]}
        return poke_dict 
    return render_template('search.html', form = form)