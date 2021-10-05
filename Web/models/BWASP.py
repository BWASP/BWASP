from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class attackVector(db.Model):
    __tablename__ = 'attackVector'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attackVector = db.Column(db.Integer, TEXT())