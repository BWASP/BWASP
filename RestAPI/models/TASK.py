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

task_db = SQLAlchemy()


class task(task_db.Model):
    __tablename__ = 'task_manager'
    __bind_key__ = 'TASK_MANAGER'

    id = task_db.Column(task_db.Integer, primary_key=True, autoincrement=True)
    targetURL = task_db.Column(task_db.TEXT, nullable=False)
    task_id = task_db.Column(task_db.Integer, unique=True, autoincrement=True)
    done = task_db.Column(task_db.BOOLEAN, default=False)

    def __init__(self, targetURL, task_id, done, **kwargs):
        self.targetURL = targetURL
        self.task_id = task_id
        self.done = done

    def __repr__(self):
        return f"<task('{self.targetURL}', '{self.task_id}', '{self.done}')>"
