from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, Length, NumberRange

class CityForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    countrycode = StringField('Country Code', validators=[DataRequired(), Length(min=3, max=3, message="Field must be 3 characters long.")])
    district = StringField('District', validators=[DataRequired(), Length(min=3, max=30)])
    population = IntegerField('Population', validators=[DataRequired(), NumberRange(min=0, max=1000000)], render_kw={"class": "form-control", "type":"number"})


class CountryForm(FlaskForm):
    code = StringField('Country Code', validators=[DataRequired(), Length(min=3, max=3, message="Field must be 3 characters long.")])
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    continent = StringField('Continent', validators=[DataRequired(), Length(min=3, max=30)])
    region = StringField('Region', validators=[DataRequired(), Length(min=3, max=30)])
    population = IntegerField('Population', validators=[DataRequired(), NumberRange(min=0, max=1000000)], render_kw={"class": "form-control", "type":"number"})
    localname = StringField('Local Name', validators=[DataRequired(), Length(min=3, max=30)])
    capital = SelectField('Capital', validators=[InputRequired(u'Please select a capital city')], render_kw={"class": "form-control"}, choices=[('', 'Select a city')])
