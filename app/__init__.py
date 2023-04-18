from flask import Flask
from config import Config
from flask_login import LoginManager
from .models import db, User
from flask_migrate import Migrate




app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

Login_Manager = LoginManager(app)

from . import routes
from . import models

@Login_Manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)