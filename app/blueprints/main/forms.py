from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PokeSearch(FlaskForm):
    search = StringField('Search Pokemon', validators=[DataRequired()])
    submit = SubmitField('Find My Pokemon')
    select = SubmitField('Confirm and Battle')