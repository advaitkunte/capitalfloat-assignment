from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint
from models import db, City, Country, Countrylanguage
from forms import CityForm
import logging
from humanize import intcomma

app_city = Blueprint('city', 'city', url_prefix='/city')

# Pagination
PER_PAGE = 20


@app_city.route("/", methods=['GET'], defaults={'_route': 'list_cities'})
@app_city.route("/<int:page>", methods=['GET'], defaults={'_route': 'list_cities'})
def cities(_route, page=1):
    '''
    All cities
    '''
    sort_by = None
    if request.args.get('sort_by', '') in ['name', 'countrycode', 'district', 'population']:
        sort_by = 'City.{}'.format(request.args.get('sort_by'))

    # if sort_by is not None:
    #     sort_by = sort_by[1:] if sort_by.startswith('-') else '-'+sort_by
        # request.args.set('sort_by', sort_by)

    cities = db.session.query(City, Country).outerjoin(
        Country, City.countrycode==Country.code).order_by(
        sort_by).paginate(page, PER_PAGE, error_out=False)
    return render_template('web/cities.html', cities=cities, intcomma=intcomma, _route=_route)

@app_city.route("/search", defaults={'_route': 'search_cities'})
@app_city.route("/search/<int:page>", defaults={'_route': 'search_cities'})
def search_city(_route, page=1):
    '''
    Search city
    '''
    city_search = request.args.get('name')
    city_search_type = request.args.get('type')

    args = []
    if city_search_type == 'name':
        args.append(City.name.contains(city_search))
    elif city_search_type == 'countrycode':
        city_search = city_search.upper()
        args.append(City.countrycode.contains(city_search))
    elif city_search_type == 'district':
        args.append(City.district.contains(city_search))

    sort_by = 'City.name'
    if request.args.get('sort_by', '') in ['name', 'countrycode', 'district', 'population']:
        sort_by = 'City.{}'.format(request.args.get('sort_by'))

    direction = ''
    if request.args.get('dir', '') in ['asc', 'desc']:
        direction = '' if request.args.get('dir')=='asc' else 'desc'

    all_cities = db.session.query(City, Country).outerjoin(
        Country, City.countrycode==Country.code).filter(
        *args).order_by(
        "{} {}".format(sort_by, direction)).paginate(
        page, PER_PAGE, error_out=False)
    return render_template('web/cities.html', cities=all_cities, intcomma=intcomma, _route=_route)

@app_city.route("/create", methods=('GET', 'POST'))
def create_city():
    '''
    Create city
    '''
    form = CityForm()
    if form.validate_on_submit():
        city = City()
        form.populate_obj(city)
        db.session.add(city)
        try:
            db.session.commit()
            flash('City created correctly', 'success')
            return redirect(url_for('city.cities', **request.args))
        except Exception as e:
            db.session.rollback()
            flash('Error creating city', 'danger')

    return render_template('web/create_city.html', form=form)

@app_city.route("/delete", methods=('POST',))
def delete_city():
    '''
    Delete city
    '''
    try:
        city = City.query.filter_by(id=request.form['id']).first()
        db.session.delete(city)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except Exception as e:
        logging.error(e, exc_info=True)
        db.session.rollback()
        flash('Error deleting city.', 'danger')

    return redirect(url_for('city.search_city', **request.args))


@app_city.route("/edit/<int:id>", methods=('GET', 'POST'))
def edit_city(id):
    '''
    Edit City
    '''
    city = City.query.filter_by(id=id).first()
    form = CityForm(obj=city)
    if form.validate_on_submit():
        try:
            form.populate_obj(city)
            db.session.add(city)
            db.session.commit()
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error updating city.', 'danger')
    return render_template(
        'web/edit_city.html',
        form=form)

