from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint
from models import db, City, Country, Countrylanguage
from forms import CountryForm
import logging
from humanize import intcomma

app_country = Blueprint('country', 'country', url_prefix='/country')

# Pagination
PER_PAGE = 20


@app_country.route("/", methods=['GET'], defaults={'_route': 'list_country'})
@app_country.route("/<int:page>", methods=['GET'], defaults={'_route': 'list_country'})
def country(_route, page=1):
    '''
    All Coutries
    '''
    sort_by = 'name'
    if request.args.get('sort_by', '') in ['name', 'code', 'continent', 'population', 'region']:
        sort_by = request.args.get('sort_by')

    countries = db.session.query(Country).order_by(
        sort_by).paginate(page, PER_PAGE, error_out=False)
    return render_template('web/countries.html', countries=countries, intcomma=intcomma, _route=_route)

@app_country.route("/search", defaults={'_route': 'search_country'})
@app_country.route("/search/<int:page>", defaults={'_route': 'search_country'})
def search_country(_route, page=1):
    '''
    Search country
    '''
    country_search = request.args.get('name', '')
    country_search_type = request.args.get('type', '')

    args = []
    if country_search_type in ['name']:
        args.append(Country.name.contains(country_search))
    elif country_search_type in ['code']:
        args.append(Country.code.contains(country_search))
    elif country_search_type in ['continent']:
        args.append(Country.continent.contains(country_search))
    elif country_search_type in ['population']:
        args.append(Country.population.contains(country_search))
    elif country_search_type in ['region']:
        args.append(Country.region.contains(country_search))

    sort_by = 'name'
    if request.args.get('sort_by', '') in ['name', 'code', 'continent', 'population', 'region']:
        sort_by = request.args.get('sort_by')

    direction = ''
    if request.args.get('dir', '') in ['asc', 'desc']:
        direction = '' if request.args.get('dir')=='asc' else 'desc'

    all_countries = db.session.query(Country).filter(
        *args).order_by("{} {}".format(sort_by, direction)
        ).paginate(
        page, PER_PAGE, error_out=False)
    return render_template('web/countries.html', countries=all_countries, intcomma=intcomma, _route=_route)

@app_country.route("/create", methods=('GET', 'POST'))
def create_country():
    '''
    Create Country
    '''
    form = CountryForm()
    form.capital.choices += [(i.id, i.name) for i in db.session.query(City).all()]

    if form.validate_on_submit():
        country = Country()
        form.populate_obj(country)
        db.session.add(country)
        try:
            db.session.commit()
            flash('City created correctly', 'success')
            return redirect(url_for('country.country', **request.args))
        except Exception as e:
            db.session.rollback()
            flash('Error creating country', 'danger')

    return render_template('web/create_country.html', form=form)

@app_country.route("/delete", methods=('POST',))
def delete_country():
    '''
    Delete country
    '''
    try:
        country = Country.query.filter_by(id=request.form['id']).first()
        db.session.delete(country)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except Exception as e:
        logging.error(e, exc_info=True)
        db.session.rollback()
        flash('Error deleting country.', 'danger')

    return redirect(url_for('country.search_country', **request.args))


@app_country.route("/edit/<int:id>", methods=('GET', 'POST'))
def edit_country(id):
    '''
    Edit Country
    '''
    country = Country.query.filter_by(id=id).first()
    form = CountryForm(obj=country)
    form.capital.choices += [(i.id, i.name) for i in db.session.query(City).all()]

    if form.validate_on_submit():
        try:
            form.populate_obj(country)
            db.session.add(country)
            db.session.commit()
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error updating country.', 'danger')
    return render_template(
        'web/edit_country.html',
        form=form)

