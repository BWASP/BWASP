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

from models.model_returnObj import bwasp_db as CSPEVALUATOR_DB


class CSPEvaluator(CSPEVALUATOR_DB.Model):
    __tablename__ = 'CSPEvaluator'
    __bind_key__ = 'BWASP'

    id = CSPEVALUATOR_DB.Column(CSPEVALUATOR_DB.Integer, primary_key=True, autoincrement=True)
    header = CSPEVALUATOR_DB.Column(CSPEVALUATOR_DB.TEXT, nullable=False)

    def __init__(self, header, **kwargs):
        self.header = header

    def __repr__(self):
        return f"<CSPEvaluator('{self.header}')>"