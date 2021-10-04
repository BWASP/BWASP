from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
class User(db.Model):
    __tablename__ = 'user'

    num = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    password = db.Column(db.String(128))
"""


class pie(db.Model):
    __tablename__ = 'pie'

    num = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    password = db.Column(db.String(128))


class area(db.Model):
    __tablename__ = 'area'

    num = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    password = db.Column(db.String(128))
