from flask import (Flask,
                   request,
                   session,
                   g,
                   redirect,
                   url_for,
                   abort,
                   render_template,
                   flash)
from flask_assets import Environment, Bundle
from unipath import Path
from contextlib import closing

DEBUG = True
SECRET_KEY = ''
APPLICATION_ROOT = '/'
BASE_DIR = Path(__file__).parent


app = Flask(__name__)
app.config.from_object(__name__)

environ = Environment(app)
environ.load_path = [Path(BASE_DIR.parent, 'static')]
environ.register(
    'javascripts',
    Bundle(
        'jquery/dist/jquery.min.js',
        'tether/dist/js/tether.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        output='bundle.js'
    )
)
environ.register(
    'stylesheets',
    Bundle(
        'bootstrap/dist/css/bootstrap.min.css',
        'Bootflat/bootflat/css/bootflat.min.css',
        Bundle(
            'styles/main.scss',
            filters ='sass'
        ),
        output='styles.css'
    )
)

# Routes ###


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
