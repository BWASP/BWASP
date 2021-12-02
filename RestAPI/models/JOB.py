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

# from RestAPI.app import db as JOB_DB
from models.model_returnObj import bwasp_db as JOB_DB


class job(JOB_DB.Model):
    __tablename__ = 'job'
    # __bind_key__ = 'BWASP'

    id = JOB_DB.Column(JOB_DB.Integer, primary_key=True, autoincrement=True)
    targetURL = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    knownInfo = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    recursiveLevel = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    uriPath = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    done = JOB_DB.Column(JOB_DB.BOOLEAN, default=False)
    maximumProcess = JOB_DB.Column(JOB_DB.TEXT, nullable=0)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, done, maximumProcess, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath
        self.done = done
        self.maximumProcess = maximumProcess

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}', '{self.done}', '{self.maximumProcess}')>"


"""
class job(bwasp_db.Model):
    __tablename__ = 'job'
    # __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    targetURL = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    knownInfo = bwasp_db.Column(bwasp_db.JSON, nullable=False)
    recursiveLevel = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    uriPath = bwasp_db.Column(bwasp_db.JSON, nullable=False)  # TEXT
    done = bwasp_db.Column(bwasp_db.BOOLEAN, default=False)
    maximumProcess = bwasp_db.Column(bwasp_db.TEXT, nullable=0)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, done, maximumProcess, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath
        self.done = done
        self.maximumProcess = maximumProcess

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}', '{self.done}', '{self.maximumProcess}')>"
"""
