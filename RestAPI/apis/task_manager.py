from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api_returnObj import Return_object
from .api_custom_fields import StringToJSON

from models.TASK import task as taskModel

ns = Namespace('api/task', description='task operations')

task = ns.model('task model', {
    'id': fields.Integer(readonly=True, description='Task initialization(task) id for unique identifier'),
    'targetURL': fields.String(required=True, description='target URL'),
    'task_id': fields.Integer(required=True, description='task id'),
    'done': fields.Integer(required=True, description='Analysis checking')
})

task_count = ns.model('Task Row Count', {
    'count': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


task_return_post_method = ns.model('task Return Post Message', {
    "message": fields.String(readonly=True, description='message of return data')
})

task_update_analysis_check = ns.model('task Update', {
    'id': fields.Integer(required=True, description='setting initialization(task) id for unique identifier'),
    'done': fields.Integer(required=True, description='Analysis checking')
})


class task_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_return_row_count(self):
        self.counter = g.task_db_obj.query(taskModel).count()
        return {"count": self.counter}

    def get(self, id=None, Type=False):
        if Type is not False and self.get_return_row_count()["count"] >= id > 0:
            self.selectData = g.task_db_obj.query(taskModel).filter(taskModel.id == id).all()
            return self.selectData

        ns.abort(404, f"task {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.task_db_obj.add(
                        taskModel(targetURL=self.insertData[ListOfData]["targetURL"],
                                  task_id=int(self.insertData[ListOfData]["task_id"]),
                                  done=int(self.insertData[ListOfData]["done"])
                                  )
                    )
                    g.task_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.task_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_task = task_data_access_object()


# task
@ns.route('')
class task_list(Resource):
    """Shows a list of all task data, and lets you POST to add new data"""

    @ns.doc('Create task')
    @ns.expect(task)
    @ns.marshal_with(task_return_post_method)
    def post(self):
        """Create task"""
        return data_access_object_for_task.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'tasks not found')
@ns.param('id', 'task id for unique identifier')
class Single_task_list(Resource):
    """Show a single task data"""

    @ns.doc('Get single task data')
    @ns.marshal_list_with(task)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_task.get(id=id, Type=True)


@ns.route('/count')
class Count_task_list(Resource):
    """Show count of all task data"""

    @ns.doc('Get count of all task data')
    @ns.marshal_with(task_count)
    def get(self):
        """Fetch a given resource"""
        return data_access_object_for_task.get_return_row_count()
        # TODO: Return Type
