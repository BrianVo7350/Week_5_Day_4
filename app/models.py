from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    pokemon = db.relationship('Pokemon', secondary = 'team', lazy = 'dynamic')
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

team = db.Table('team',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable = False),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id'), nullable = False))   


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokename = db.Column(db.String(30), nullable = False)
    #type = db.Column(db.String(30), nullable = False)
    ability = db.Column(db.String(20), nullable = False)
    attack = db.Column(db.Integer, nullable = False)
    defense = db.Column(db.Integer, nullable = False)
    hp = db.Column(db.Integer, nullable = False)
    photo = db.Column(db.String(100), nullable = False)
    
    def saveToDB(self):
         db.session.add(self)
         db.session.commit()

    def deleteFromDB(self):
         db.session.delete(self)
         db.session.commit()
    
    def from_dict(self, poke_dict):
        self.id = poke_dict['id']
        self.pokename = poke_dict['name']
        self.ability = poke_dict['ability']
        self.attack = poke_dict['attack']
        self.defense = poke_dict['defense']
        self.hp = poke_dict['hp']
        self.photo = poke_dict['photo']
    
    def known_pokemon(name):
        return Pokemon.query.filter_by(pokename = name ).first()
        




