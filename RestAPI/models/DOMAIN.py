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

# from RestAPI.app import db as DOMAIN_DB
from models.model_returnObj import bwasp_db as DOMAIN_DB


class domain(DOMAIN_DB.Model):
    __tablename__ = 'domain'
    # __bind_key__ = 'BWASP'

    id = DOMAIN_DB.Column(DOMAIN_DB.Integer, primary_key=True, autoincrement=True)
    related_Packet = DOMAIN_DB.Column(DOMAIN_DB.Integer, nullable=False)
    URL = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)
    URI = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)
    action_URL = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)  # TEXT
    action_URL_Type = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)  # TEX T
    params = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)  # TEXT
    comment = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)
    attackVector = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)
    impactRate = DOMAIN_DB.Column(DOMAIN_DB.Integer, nullable=False)
    description = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)
    Details = DOMAIN_DB.Column(DOMAIN_DB.TEXT, nullable=False)

    def __init__(self, related_Packet, URL, URI, action_URL, action_URL_Type, params, comment, attackVector, impactRate, description, Details, **kwargs):
        self.related_Packet = related_Packet
        self.URL = URL
        self.URI = URI
        self.action_URL = action_URL
        self.action_URL_Type = action_URL_Type
        self.params = params
        self.comment = comment
        self.attackVector = attackVector
        self.impactRate = impactRate
        self.description = description
        self.Details = Details

    def __repr__(self):
        return f"<domain('{self.related_Packet}', '{self.URL}', '{self.URI}', '{self.action_URL}', '{self.action_URL_Type}', '{self.params}', '{self.comment}', " \
               f"'{self.attackVector}', '{self.impactRate}', '{self.description}', '{self.Details}')>"


"""
class domain(bwasp_db.Model):
    __tablename__ = 'domain'
    # __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    related_Packet = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    URL = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    URI = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    action_URL = bwasp_db.Column(bwasp_db.JSON, nullable=False)  # TEXT
    action_URL_Type = bwasp_db.Column(bwasp_db.JSON, nullable=False)  # TEX T
    params = bwasp_db.Column(bwasp_db.JSON, nullable=False)  # TEXT
    comment = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    attackVector = bwasp_db.Column(bwasp_db.JSON, nullable=False)
    impactRate = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    description = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    Details = bwasp_db.Column(bwasp_db.JSON, nullable=False)

    def __init__(self, related_Packet, URL, URI, action_URL, action_URL_Type, params, comment, attackVector, impactRate, description, Details, **kwargs):
        self.related_Packet = related_Packet
        self.URL = URL
        self.URI = URI
        self.action_URL = action_URL
        self.action_URL_Type = action_URL_Type
        self.params = params
        self.comment = comment
        self.attackVector = attackVector
        self.impactRate = impactRate
        self.description = description
        self.Details = Details

    def __repr__(self):
        return f"<domain('{self.related_Packet}', '{self.URL}', '{self.URI}', '{self.action_URL}', '{self.action_URL_Type}', '{self.params}', '{self.comment}', " \
               f"'{self.attackVector}', '{self.impactRate}', '{self.description}', '{self.Details}')>"
"""