from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import job as jobModel

ns = Namespace('api/job', description='job operations')

job = ns.model('Job', {
    'id': fields.Integer(readonly=True, description='setting initialization(Job) id for unique identifier'),
    'targetURL': fields.String(required=True, description='target URL'),
    'knownInfo': fields.String(required=True, description='Known information'),
    'recursiveLevel': fields.String(required=True, description='recursive level'),
    'uriPath': fields.String(required=True, description='Path on Web Server')
})


class JobDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            self.selectData = g.BWASP_DBObj.query(jobModel).all()
            return self.selectData

        if Type is not False and id > 0:
            self.selectData = g.BWASP_DBObj.query(jobModel).filter(jobModel.id == id).all()
            return self.selectData

        ns.abort(404, f"job {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        jobModel(targetURL=self.insertData[ListOfData]["targetURL"],
                                 knownInfo=self.insertData[ListOfData]["knownInfo"],
                                 recursiveLevel=self.insertData[ListOfData]["recursiveLevel"],
                                 uriPath=self.insertData[ListOfData]["uriPath"]
                                 )
                    )
                    g.BWASP_DBObj.commit()
                return self.insertData
            except:
                g.BWASP_DBObj.rollback()

        if str(type(data)) == "<class 'dict'>":
            self.insertData = data
            try:
                g.BWASP_DBObj.add(
                    jobModel(targetURL=self.insertData["targetURL"],
                             knownInfo=self.insertData["knownInfo"],
                             recursiveLevel=self.insertData["recursiveLevel"],
                             uriPath=self.insertData["uriPath"]
                             )
                )
                g.BWASP_DBObj.commit()
                return self.insertData
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData


Job_DAO = JobDAO()


# Job
@ns.route('')
class JobList(Resource):
    """Shows a list of all job data, and lets you POST to add new data"""

    @ns.doc('List of all Job data')
    @ns.marshal_list_with(job)
    def get(self):
        """Shows Job data"""
        return Job_DAO.get()

    @ns.doc('Create Job')
    @ns.expect(job)
    @ns.marshal_with(job, code=201)
    def post(self):
        """Create Job"""
        return Job_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Jobs not found')
@ns.param('id', 'Job id for unique identifier')
class single_JobList(Resource):
    """Show a single Job data"""

    @ns.doc('Get single Job data')
    @ns.marshal_with(job)
    def get(self, id):
        """Fetch a given resource"""
        return Job_DAO.get(id, Type=True)
