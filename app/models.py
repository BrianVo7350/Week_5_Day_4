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

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()


    class Pokemon(db.Model):
      id = db.Column(db.integer, primary_key=True)
      pokename = db.Column(db.String(30), nullable = False)
      type = db.Column(db.String(30), nullable = False)
      ability = db.Column(db.String(20), nullable = False)
      attack = db.Column(db.String(20), nullable = False)
      defense = db.Column(db.String(20), nullable = False)
      hp = db.Column(db.String(20), nullable = False)
#     photo = db.Column(db.String(100), nullable = False)

      def __init__(self, id, pokename, type, ability, attack, defense, hp, photo):
        self.pokemname = pokename
        self.type = type
        self.ability = ability
        self.attack = attack
        self.defense = defense
        self.hp = hp
#         self.photo = photo 
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()