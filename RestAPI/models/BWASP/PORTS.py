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

from model_returnObj import bwasp_db as PORTS_DB


class ports(PORTS_DB.Model):
    __tablename__ = 'ports'
    __bind_key__ = 'BWASP'

    id = PORTS_DB.Column(PORTS_DB.Integer, primary_key=True, autoincrement=True)
    service = PORTS_DB.Column(PORTS_DB.TEXT, nullable=False)
    target = PORTS_DB.Column(PORTS_DB.TEXT, nullable=False)
    port = PORTS_DB.Column(PORTS_DB.TEXT, nullable=False)
    result = PORTS_DB.Column(PORTS_DB.TEXT, nullable=False)

    def __init__(self, service, target, port, result, **kwargs):
        self.service = service
        self.target = target
        self.port = port
        self.result = result

    def __repr__(self):
        return f"<ports('{self.service}', '{self.target}', '{self.port}, {self.result}')>"

