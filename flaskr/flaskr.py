from flask import (Flask,
                   request,
                   session,
                   redirect,
                   url_for,
                   flash,
                   render_template)
import requests
from flask_assets import Environment, Bundle
from unipath import Path
from werkzeug.utils import secure_filename
import hashlib


def startedAt(gasList, costList):
    gasSum = costSum = tank = 0
    firstStation = 1
    for i in range(len(gasList)):
        gasSum += gasList[i]
        costSum += costList[i]
        tank += gasList[i] - costList[i]
        if tank < 0:
            tank = 0
            firstStation += i
    if gasSum < costSum:
        return 'impossible'
    return firstStation


def GasStation(strArr):
    inputString = strArr
    data = inputString.replace('"', '').split(',')
    N = int(data.pop(0))
    if N < 2:
        raise Exception('Invalid number for gas station')
    components = [[int(itemPart) for itemPart in item.split(':')]
                  for item in data]
    stationStock = []
    totalConsumed = []
    for component in components:
        if len(component) < 2:
            raise Exception('Invalid format')
        stationStock.append(component[0])
        totalConsumed.append(component[1])
    return startedAt(stationStock, totalConsumed)


def validate_filename(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

DEBUG = True
SECRET_KEY = hashlib.md5('SECRET_KEY'.encode('utf-8')).hexdigest()
APPLICATION_ROOT = '/'
BASE_DIR = Path(__file__)
UPLOAD_DIR = Path(BASE_DIR.parent, 'uploads')
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config.from_object(__name__)

environ = Environment(app)
environ.load_path = [Path(BASE_DIR.parent.parent, 'static')]
environ.register(
    'javascripts',
    Bundle(
        'jquery/dist/jquery.min.js',
        'tether/dist/js/tether.min.js',
        'bootstrap/dist/js/bootstrap.min.js',
        'scripts/main.js',
        output='bundle.js'
    )
)
environ.register(
    'stylesheets',
    Bundle(
        'bootstrap/dist/css/bootstrap.min.css',
        'Bootflat/bootflat/css/bootflat.min.css',
        Bundle(
            'styles/sass/main.scss',
            filters='pyscss'
        ),
        output='styles.css'
    )
)

# Routes ###


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file was sent')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('File field was empty')
            return redirect(url_for('index'))
        if file and validate_filename(file.filename):
            filename = secure_filename(file.filename)
            file.save(Path(UPLOAD_DIR, filename))
            f = Path(UPLOAD_DIR, filename)
            results = {}
            try:
                with open(f) as strings:
                    for line in strings:
                        if line:
                            results[line] = GasStation(line)
            except Exception as e:
                flash('The file is incorrectly structured')
                return redirect(url_for('index'))
            return render_template('result.html', results=results)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
