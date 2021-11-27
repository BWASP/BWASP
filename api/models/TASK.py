from flask_sqlalchemy import SQLAlchemy

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import db as task_db


class task(task_db.Model):
    __tablename__ = 'task'
    __bind_key__ = 'TASK'

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
