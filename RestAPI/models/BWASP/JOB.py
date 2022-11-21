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

from .model_returnObj import bwasp_db as JOB_DB


class job(JOB_DB.Model):
    __tablename__ = 'job'
    __bind_key__ = 'BWASP'

    id = JOB_DB.Column(JOB_DB.Integer, primary_key=True, autoincrement=True)
    targetURL = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    knownInfo = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    recursiveLevel = JOB_DB.Column(JOB_DB.TEXT, nullable=False)
    done = JOB_DB.Column(JOB_DB.BOOLEAN, default=0, nullable=False)
    maximumProcess = JOB_DB.Column(JOB_DB.TEXT, nullable=False)

    def __init__(self, targetURL, knownInfo, recursiveLevel, done, maximumProcess, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.done = done
        self.maximumProcess = maximumProcess

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.done}', '{self.maximumProcess}')>"
