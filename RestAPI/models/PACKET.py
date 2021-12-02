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

# from RestAPI.app import db as PACKET_DB
from models.model_returnObj import bwasp_db as PACKET_DB


class packet(PACKET_DB.Model):
    __tablename__ = 'packets'
    # __bind_key__ = 'BWASP'

    id = PACKET_DB.Column(PACKET_DB.Integer, primary_key=True, autoincrement=True)
    category = PACKET_DB.Column(PACKET_DB.Integer, nullable=False)
    statusCode = PACKET_DB.Column(PACKET_DB.Integer, nullable=False)
    requestType = PACKET_DB.Column(PACKET_DB.TEXT, nullable=False)
    requestJson = PACKET_DB.Column(PACKET_DB.TEXT, nullable=False)
    responseHeader = PACKET_DB.Column(PACKET_DB.TEXT, nullable=False)
    responseBody = PACKET_DB.Column(PACKET_DB.TEXT, nullable=False)

    def __init__(self, category, statusCode, requestType, requestJson, responseHeader, responseBody, **kwargs):
        self.category = category
        self.statusCode = statusCode
        self.requestType = requestType
        self.requestJson = requestJson
        self.responseHeader = responseHeader
        self.responseBody = responseBody

    def __repr__(self):
        return f"<packet('{self.category}', '{self.statusCode}', '{self.requestType}', '{self.requestJson}', " \
               f"'{self.responseHeader}', '{self.responseBody}')>"


"""
class packets(bwasp_db.Model):
    __tablename__ = 'packets'
    # __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    category = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    statusCode = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    requestType = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    requestJson = bwasp_db.Column(bwasp_db.JSON, nullable=False)
    responseHeader = bwasp_db.Column(bwasp_db.JSON, nullable=False)
    responseBody = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

    def __init__(self, category, statusCode, requestType, requestJson, responseHeader, responseBody, **kwargs):
        self.category = category
        self.statusCode = statusCode
        self.requestType = requestType
        self.requestJson = requestJson
        self.responseHeader = responseHeader
        self.responseBody = responseBody

    def __repr__(self):
        return f"<packets('{self.category}', '{self.statusCode}', '{self.requestType}', '{self.requestJson}', " \
               f"'{self.responseHeader}', '{self.responseBody}')>"

"""
