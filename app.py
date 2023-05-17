from flask import Flask, flash, request, redirect, render_template, url_for, make_response
from flask_navigation import Navigation
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import InputRequired, Length, NumberRange, ValidationError
import pdfkit, uuid, datetime
import pandas as pd

# Define path to wkhtmltopdf.exe
path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Point pdfkit configuration to wkhtmltopdf.exe
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

app = Flask(__name__)
# app.secret_key = 'T-a8iISqWnNnTDI4FcVazw'
nav = Navigation(app)
csrf = CSRFProtect(app)

foo = uuid.uuid4().hex
app.secret_key = foo


nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Guides', 'guides'),
    nav.Item('Scripts', 'scripts')
])

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        f = request.files['fileUpload']

        if f.filename == '':
            return redirect(request.url)

        elif f and not allowed_file(f.filename):
            return redirect(request.url)

        elif f and allowed_file(f.filename):
            index.filename = secure_filename(f.filename)
            df = pd.read_csv(index.filename, keep_default_na=False)
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

            index.solutions = {}
            for main_key, values in flipped_result['Solution'].items():
                for key, value in result['Host'].items():
                    for i in values:
                        if i == key:
                            if main_key not in index.solutions:
                                index.solutions[main_key] = [value]
                            if value not in index.solutions[main_key]:
                                index.solutions[main_key].append(value)

            index.hosts = {}
            for main_key, values in flipped_result['Host'].items():
                for key, value in result['Solution'].items():
                    for i in values:
                        if i == key:
                            if main_key not in index.hosts:
                                index.hosts[main_key] = [value]
                            if value not in index.hosts[main_key]:
                                index.hosts[main_key].append(value)

            index.risks = {}
            for main_key, values in flipped_result['Risk'].items():
                for key, value in result['Solution'].items():
                    for i in values:
                        if i == key:
                            if main_key not in index.risks:
                                index.risks[main_key] = [value]
                            if value not in index.risks[main_key]:
                                index.risks[main_key].append(value)

            index.form = ReportForm()

            # return render_template('analysis.html', filename=index.filename, solutions=index.solutions, hosts=index.hosts, risks=index.risks, result=result, flipped_result=flipped_result, form=index.form)
            return redirect(url_for('analysis'))
    else:
        return render_template('index.html')


class ReportForm(FlaskForm):
    companyname = StringField('Company Name', validators=[InputRequired(), Length(min=2, max=200)], render_kw={"placeholder": "Enter the company's name here"})
    companyalias = StringField('Company Alias', validators=[InputRequired(), Length(min=2, max=30)])
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=[InputRequired()])
    enddate = DateField('End Date', format='%Y-%m-%d', validators=[InputRequired()])
    hostnum = IntegerField('Number of Hosts', validators=[InputRequired(), NumberRange(min=1)])
    generate = SubmitField('Generate Report')

    def validate_on_submit(form):
        if form.enddate.data < form.startdate.data:
            flash(u"Please take note that the end date should not be earlier than the start date.")
        else:
            return True


@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        if request.form['companyname'] != '' and request.form['startdate'] != '' and request.form['enddate'] != '':
            form = ReportForm(request.form)
            if form.validate_on_submit():
                companyname = request.form['companyname']
                companyalias = request.form['companyalias']
                startdate = request.form['startdate']
                enddate = request.form['enddate']
                start_date = datetime.datetime.strptime(startdate, '%Y-%m-%d')
                start_date = start_date.strftime('%d %b %Y')
                end_date = datetime.datetime.strptime(enddate, '%Y-%m-%d')
                end_date = end_date.strftime('%d %b %Y')
                num_hosts = request.form['hostnum']
                sol_list = list(index.solutions.keys())
                html = render_template('report.html', solutions=index.solutions, risks=index.risks, sol_list=sol_list, companyname=companyname, companyalias=companyalias, startdate=start_date, enddate=end_date, num_hosts=num_hosts)
                css = 'static/css/report.css'
                pdf = pdfkit.from_string(html, False, css=css, configuration=config)
                response = make_response(pdf)
                response.headers["Content-Type"] = "application/pdf"
                response.headers["Content-Disposition"] = "attachment; filename=report.pdf"
                return response
            else:
                return redirect(url_for('analysis'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/analysis')
def analysis():
    return render_template('analysis.html', filename=index.filename, solutions=index.solutions, hosts=index.hosts, risks=index.risks, form=index.form)


@app.route('/guides')
def guides():
    return render_template('guides.html')


@app.route('/scripts')
def scripts():
    return render_template('scripts.html')


if __name__ == "__main__":
    app.run(debug=True)
