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

from models.BWASP.model_returnObj import task_db as TASK_MANAGER_DB


class task(TASK_MANAGER_DB.Model):
    __tablename__ = 'task_manager'
    __bind_key__ = 'TASK_MANAGER'

    id = TASK_MANAGER_DB.Column(TASK_MANAGER_DB.Integer, primary_key=True, autoincrement=True)
    targetURL = TASK_MANAGER_DB.Column(TASK_MANAGER_DB.TEXT, nullable=False)
    subURL = TASK_MANAGER_DB.Column(TASK_MANAGER_DB.TEXT, nullable=False)
    task_id = TASK_MANAGER_DB.Column(TASK_MANAGER_DB.TEXT, nullable=False, unique=True)

    def __init__(self, targetURL, subURL, task_id, **kwargs):
        self.targetURL = targetURL
        self.subURL = subURL
        self.task_id = task_id

    def __repr__(self):
        return f"<task('{self.targetURL}', '{self.subURL}', '{self.task_id}', '{self.done}')>"
