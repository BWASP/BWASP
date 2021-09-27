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


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/404')
def NotFound():
    return render_template('404.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
