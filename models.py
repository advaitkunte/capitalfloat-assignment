from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('city_id_seq'::regclass)"))
    name = db.Column(db.Text, nullable=False)
    countrycode = db.Column(db.CHAR(3), nullable=False)
    district = db.Column(db.Text, nullable=False)
    population = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<City %r>' % self.name

    @db.validates('countrycode')
    def convert_upper(self, key, value):
        return value.upper()


class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = (
        db.CheckConstraint("((((((continent = 'Asia'::text) OR (continent = 'Europe'::text)) OR (continent = 'North America'::text)) OR (continent = 'Africa'::text)) OR (continent = 'Oceania'::text)) OR (continent = 'Antarctica'::text)) OR (continent = 'South America'::text)"),
    )

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('country_id_seq'::regclass)"))
    code = db.Column(db.CHAR(3), primary_key=True)
    name = db.Column(db.Text, nullable=False)
    continent = db.Column(db.Text, nullable=False)
    region = db.Column(db.Text, nullable=False)
    surfacearea = db.Column(db.Float, nullable=False)
    indepyear = db.Column(db.SmallInteger)
    population = db.Column(db.Integer, nullable=False)
    lifeexpectancy = db.Column(db.Float)
    gnp = db.Column(db.Numeric(10, 2))
    gnpold = db.Column(db.Numeric(10, 2))
    localname = db.Column(db.Text, nullable=False)
    governmentform = db.Column(db.Text, nullable=False)
    headofstate = db.Column(db.Text)
    capital = db.Column(db.ForeignKey(u'city.id'))
    code2 = db.Column(db.CHAR(2), nullable=False)

    city = db.relationship(u'City', backref=db.backref('city_to_country', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Country %r>' % self.name


class Countrylanguage(db.Model):
    __tablename__ = 'countrylanguage'

    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('country_id_seq'::regclass)"))
    countrycode = db.Column(db.ForeignKey(u'country.code'), primary_key=True, nullable=False)
    language = db.Column(db.Text, primary_key=True, nullable=False)
    isofficial = db.Column(db.Boolean, nullable=False)
    percentage = db.Column(db.Float, nullable=False)

    country = db.relationship(u'Country', backref=db.backref('country_to_countrylanguage', cascade='all, delete-orphan'))

    def __repr__(self):
        return '<Country Language %r>' % self.name

