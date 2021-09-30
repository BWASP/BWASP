# Flask version 2.0.1
# Flask-SQLAlchemy version 2.5.1

import os
from models import db
from flask import (
    Flask, render_template,
    url_for
)

app = Flask(__name__)

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(16)

db.init_app(app)
db.app = app
db.create_all()


@app.route('/start')
def mode_selection():
    return render_template('./common/mode_selection.html')


@app.route('/common/export')
def CommonExport():
    return render_template('./common/export.html')


@app.route('/automation/options')
def manual_options():
    return render_template('./automation/options.html', Title="자동 분석 옵션 설정 - BWASP")


@app.route('/AttackVector')
def attack_Vector():
    return render_template('./AttackVector.html')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/404')
def NotFound():
    return render_template('404.html')


@app.route('/blank')
def blank():
    return render_template('blank.html')


@app.route('/buttons')
def buttons():
    return render_template('buttons.html')


@app.route('/cards')
def cards():
    return render_template('cards.html')


@app.route('/charts')
def charts():
    return render_template('charts.html')


@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot-password.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/tables')
def tables():
    return render_template('tables.html')


@app.route('/utilities_animation')
def utilities_animation():
    return render_template('utilities-animation.html')


@app.route('/utilities_border')
def utilities_border():
    return render_template('utilities-border.html')


@app.route('/utilities_color')
def utilities_color():
    return render_template('utilities-color.html')


@app.route('/utilities_other')
def utilities_other():
    return render_template('utilities-other.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
