from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from flask_login import Usermixin

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    post = db.relationship('Post')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

#class Pokemon(db.Model):
    #id = db.Column(db.integer, primary_key=True)
    #pokename = db.Column(db.String(30), nullable = False)
    #type = db.Column(db.String(30), nullable = False)

    #def __init__(self, pokename, type):
        #self.pokemname = pokename
        #self.type = type
    
    #def saveToDB(self):
        #db.session.add(self)
        #db.session.commit()
    