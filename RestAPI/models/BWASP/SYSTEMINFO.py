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

from .model_returnObj import bwasp_db as SYSTEMINFO_DB


class systeminfo(SYSTEMINFO_DB.Model):
    __tablename__ = 'systeminfo'
    __bind_key__ = 'BWASP'

    id = SYSTEMINFO_DB.Column(SYSTEMINFO_DB.Integer, primary_key=True, autoincrement=True)
    url = SYSTEMINFO_DB.Column(SYSTEMINFO_DB.TEXT, nullable=False)
    data = SYSTEMINFO_DB.Column(SYSTEMINFO_DB.TEXT, nullable=False)

    def __init__(self, url, data, **kwargs):
        self.url = url
        self.data = data

    def __repr__(self):
        return f"<systeminfo('{self.url}', '{self.data}')>"
