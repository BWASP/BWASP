from flask_sqlalchemy import SQLAlchemy

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import db as cve_db


# cve_db = SQLAlchemy()


class cve(cve_db.Model):
    __tablename__ = 'CVE'
    __bind_key__ = 'CVE'
    id = cve_db.Column(cve_db.Integer, primary_key=True, autoincrement=True)
    year = cve_db.Column(cve_db.TEXT, nullable=False)
    description = cve_db.Column(cve_db.TEXT, nullable=False)
