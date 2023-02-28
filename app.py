from flask import Flask, request, render_template, url_for
from flask_navigation import Navigation
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Guides', 'guides'),
    nav.Item('Scripts', 'scripts')
])

@app.route('/')
def index():
    return render_template('index.html')
