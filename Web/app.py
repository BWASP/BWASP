# Flask version 2.0.1
# Flask-SQLAlchemy version 2.5.1

import os
from models import db
from flask import Flask, render_template

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


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/')
def main():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


