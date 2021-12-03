# -*- coding: utf-8 -*-

"""
    package.module
    ~~~~~~~~~~~~~~

    A brief description goes here.

    :copyright: (c) YEAR by AUTHOR.
    :license: LICENSE_NAME, see LICENSE_FILE for more details.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.model_returnObj import cve_db as CVELIST_DB


class cve(CVELIST_DB.Model):
    __tablename__ = 'cvelist'
    __bind_key__ = 'CVELIST'

    id = CVELIST_DB.Column(CVELIST_DB.Integer, primary_key=True, autoincrement=True)
    year = CVELIST_DB.Column(CVELIST_DB.TEXT, nullable=False)
    description = CVELIST_DB.Column(CVELIST_DB.TEXT, nullable=False)
