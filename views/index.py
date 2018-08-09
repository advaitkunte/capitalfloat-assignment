from flask import Flask, redirect, url_for, Blueprint
import logging

app_index = Blueprint('index', 'index', url_prefix='/')


@app_index.route("/", methods=['GET'])
def index():
    return redirect(url_for('city.cities'))

