# coding: utf-8
from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, Float, ForeignKey, Integer, Numeric, SmallInteger, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    countrycode = Column(CHAR(3), nullable=False)
    district = Column(Text, nullable=False)
    population = Column(Integer, nullable=False)


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        CheckConstraint("((((((continent = 'Asia'::text) OR (continent = 'Europe'::text)) OR (continent = 'North America'::text)) OR (continent = 'Africa'::text)) OR (continent = 'Oceania'::text)) OR (continent = 'Antarctica'::text)) OR (continent = 'South America'::text)"),
    )

    code = Column(CHAR(3), primary_key=True)
    name = Column(Text, nullable=False)
    continent = Column(Text, nullable=False)
    region = Column(Text, nullable=False)
    surfacearea = Column(Float, nullable=False)
    indepyear = Column(SmallInteger)
    population = Column(Integer, nullable=False)
    lifeexpectancy = Column(Float)
    gnp = Column(Numeric(10, 2))
    gnpold = Column(Numeric(10, 2))
    localname = Column(Text, nullable=False)
    governmentform = Column(Text, nullable=False)
    headofstate = Column(Text)
    capital = Column(ForeignKey(u'city.id'))
    code2 = Column(CHAR(2), nullable=False)

    city = relationship(u'City')


class Countrylanguage(Base):
    __tablename__ = 'countrylanguage'

    countrycode = Column(ForeignKey(u'country.code'), primary_key=True, nullable=False)
    language = Column(Text, primary_key=True, nullable=False)
    isofficial = Column(Boolean, nullable=False)
    percentage = Column(Float, nullable=False)

    country = relationship(u'Country')

