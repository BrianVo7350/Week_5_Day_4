from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf import FlaskForm

class Pokemon_search(FlaskForm):
    pokemon_name = StringField('What Pokemon would you like to search for?: ', validators=[DataRequired()])
    submit = SubmitField('Search')

#class Pokemon_battle(FlaskForm):

