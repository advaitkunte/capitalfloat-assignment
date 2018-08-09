from flask import Flask
from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from views.index import app_index
from views.city import app_city
from views.country import app_country

from models import db

# Flask
app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG_FILE')
db.init_app(app)

app.register_blueprint(app_index)
app.register_blueprint(app_city)
app.register_blueprint(app_country)


@app.route('/')
def index():
    return 'The URL for this page is {}'.format(url_for('index'))

def simple(env, resp):
    resp(b'200 OK', [(b'Content-Type', b'text/plain')])
    return [b'Hello WSGI World']

app.wsgi_app = DispatcherMiddleware(simple, {'/capital-float-assignment': app.wsgi_app})


if __name__ == '__main__':
    app.run()