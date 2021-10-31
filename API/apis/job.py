from flask import (
    Flask, g, jsonify
)
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
from models.BWASP import job as jobModel

ns = Namespace('api/job', description='job operations')

job = ns.model('Job', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'targetURL': fields.String(required=True, description='The task details'),
    'knownInfo': fields.String(required=True, description='The task details'),
    'recursiveLevel': fields.String(required=True, description='The task details'),
    'uriPath': fields.String(required=True, description='The task details')
})

class JobDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.jobs = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            job = g.BWASP_DBObj.query(jobModel).all()
            print(len(job))
            return job
        elif Type is not False and id > 0:
            job = g.BWASP_DBObj.query(jobModel).filter(jobModel.id == id).all()
            return job
        else:
            ns.abort(404, f"job {id} doesn't exist")

    def create(self, data):
        job = data
        g.BWASP_DBObj.add(
            jobModel(targetURL=job["targetURL"],
                     knownInfo=job["knownInfo"],
                     recursiveLevel=job["recursiveLevel"],
                     uriPath=job["uriPath"]
                     )
        )
        g.BWASP_DBObj.commit()
        return job

Job_DAO = JobDAO()

# Job
@ns.route('')
class JobList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ns.doc('list_Jobs')
    @ns.marshal_list_with(job)
    def get(self):
        """List all tasks"""
        return Job_DAO.get()

    @ns.doc('create_Jobs')
    @ns.expect(job)
    @ns.marshal_with(job, code=201)
    def post(self):
        """Create a new task"""
        return Job_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Jobs not found')
@ns.param('id', 'The task identifier')
class Job(Resource):
    """Show a single job item and lets you delete them"""

    @ns.doc('get_packet')
    @ns.marshal_with(job)
    def get(self, id):
        """Fetch a given resource"""
        return Job_DAO.get(id, Type=True)
