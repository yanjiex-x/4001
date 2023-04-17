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

@app.route('/', methods=('POST', 'GET'))
def index():
    if request.method == 'POST':
        f = request.files['fileUpload']
        filename = secure_filename(f.filename)
        df = pd.read_csv(filename, keep_default_na=False)
        result = df.to_dict()
        flipped_result = {}
        for key, value in result.items():
            flipped = {}
            for k, v in value.items():
                if v not in flipped:
                    flipped[v] = [k]
                else:
                    flipped[v].append(k)
            flipped_result[key] = flipped

        solutions = {}
        for main_key, values in flipped_result['Solution'].items():
            for key, value in result['Host'].items():
                for i in values:
                    if i == key:
                        if main_key not in solutions:
                            solutions[main_key] = [value]
                        if value not in solutions[main_key]:
                            solutions[main_key].append(value)

        hosts = {}
        for main_key, values in flipped_result['Host'].items():
            for key, value in result['Solution'].items():
                for i in values:
                    if i == key:
                        if main_key not in hosts:
                            hosts[main_key] = [value]
                        if value not in hosts[main_key]:
                            hosts[main_key].append(value)

        risks = {}
        for main_key, values in flipped_result['Risk'].items():
            for key, value in result['Solution'].items():
                for i in values:
                    if i == key:
                        if main_key not in risks:
                            risks[main_key] = [value]
                        if value not in risks[main_key]:
                            risks[main_key].append(value)


        return render_template('analysis.html', filename=filename, solutions=solutions, hosts=hosts, risks=risks)
    else:
        return render_template('index.html')

@app.route('/scripts')
def scripts():
    return render_template('scripts.html')


if __name__ == "__main__":
    app.run(debug=True)
