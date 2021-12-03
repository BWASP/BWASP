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
    task_id = TASK_MANAGER_DB.Column(TASK_MANAGER_DB.TEXT, nullable=False, unique=True)

    def __init__(self, targetURL, task_id, done, **kwargs):
        self.targetURL = targetURL
        self.task_id = task_id

    def __repr__(self):
        return f"<task('{self.targetURL}', '{self.task_id}', '{self.done}')>"


"""
{
  "tool": {
    "analysisLevel": 1624,
    "optionalJobs": [
      "CSPEvaluate",
      "portScan",
      "testPayloads"
    ]
  },
  "info": [
    {
      "name": "PHP",
      "version": "5.0"
    },
    {
      "name": "MariaDB",
      "version": "1.0"
    }
  ],
  "target": "http://suninatas.com/",
  "API": {
    "google": {
      "key": "1",
      "engineId": "21"
    }
  },
  "maximumProcess": 6
}
"""
