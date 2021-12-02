# -*- coding: utf-8 -*-

"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""

from flask_sqlalchemy import SQLAlchemy

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

cve_db = SQLAlchemy()


class cve(cve_db.Model):
    __tablename__ = 'cvelist'
    __bind_key__ = 'CVELIST'

    id = cve_db.Column(cve_db.Integer, primary_key=True, autoincrement=True)
    year = cve_db.Column(cve_db.TEXT, nullable=False)
    description = cve_db.Column(cve_db.TEXT, nullable=False)
