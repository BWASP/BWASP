from flask import g
from flask_restx import Resource, fields, Namespace, model
from .api_returnObj import Return_object
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import job as jobModel

ns = Namespace('api/job', description='job operations')

job = ns.model('job model', {
    'id': fields.Integer(readonly=True, description='setting initialization(Job) id for unique identifier'),
    'targetURL': fields.String(required=True, description='target URL'),
    'knownInfo': fields.String(required=True, description='Known information'),
    'recursiveLevel': fields.String(required=True, description='recursive level'),
    'uriPath': fields.String(required=True, description='Path on Web Server')
})

job_return_post_method = ns.model('Job Return Post Message', {
    "message": fields.String(readonly=True, description='message of return data')
})


class Job_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_return_row_count(self):
        self.counter = g.bwasp_db_obj.query(jobModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(jobModel).all()
            return self.selectData

        if Type is not False and self.get_return_row_count() >= id > 0:
            self.selectData = g.bwasp_db_obj.query(jobModel).filter(jobModel.id == id).all()
            return self.selectData

        ns.abort(404, f"job {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        jobModel(targetURL=str(self.insertData[ListOfData]["targetURL"]),
                                 knownInfo=json.dumps(self.insertData[ListOfData]["knownInfo"]),
                                 recursiveLevel=str(self.insertData[ListOfData]["recursiveLevel"]),
                                 uriPath=str(self.insertData[ListOfData]["uriPath"])
                                 )
                    )
                    g.bwasp_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_job = Job_data_access_object()


# Job
@ns.route('')
class Job_list(Resource):
    """Shows a list of all job data, and lets you POST to add new data"""

    @ns.doc('List of all Job data')
    @ns.marshal_list_with(job)
    def get(self):
        """Shows Job data"""
        return data_access_object_for_job.get(id=None, Type=False)

    @ns.doc('Create Job')
    @ns.expect(job)
    @ns.marshal_with(job_return_post_method)
    def post(self):
        """Create Job"""
        return data_access_object_for_job.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'Jobs not found')
@ns.param('id', 'Job id for unique identifier')
class Single_job_list(Resource):
    """Show a single Job data"""

    @ns.doc('Get single Job data')
    @ns.marshal_list_with(job)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_job.get(id=id, Type=True)
