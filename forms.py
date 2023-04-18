from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

class Pokemon_search(FlaskForm):
    pokemon_name = StringField('What Pokemon would you like to search for?: ', validators=[DataRequired()])
    submit = SubmitField('Search')

class Signup(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField()

