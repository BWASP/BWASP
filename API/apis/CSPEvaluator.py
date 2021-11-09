from flask import g
from flask_restx import Resource, fields, Namespace, model
from sqlalchemy import func
from .api_returnObj import ReturnObject
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import CSPEvaluator as CSPEvaluatorModel

ns = Namespace('api/cspevaluator', description='csp evaluator operations')

CSPEvaluator = ns.model('CSPEvaluator', {
    'id': fields.Integer(readonly=True, description='CspEvaluator id for unique identifier'),
    'header': fields.String(required=True, description='Content-Security Policy in HTTP header')
})

CSPEvaluator_returnPost = ns.model('CSPEvaluator_returnPost', {
    "message": fields.String(readonly=True, description='message of return data')
})


class CSPEvaluatorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_retRowCount(self):
        self.counter = g.BWASP_DBObj.query(CSPEvaluatorModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.BWASP_DBObj.query(CSPEvaluatorModel).all()
            return self.selectData

        if Type is not False and self.get_retRowCount() >= id > 0:
            self.selectData = g.BWASP_DBObj.query(CSPEvaluatorModel).filter(CSPEvaluatorModel.id == id).all()
            return self.selectData

        ns.abort(404, f"CSPEvaluator data {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        CSPEvaluatorModel(
                            header=json.dumps(self.insertData[ListOfData]["header"])
                        )
                    )
                    g.BWASP_DBObj.commit()

                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)


CSPEvaluator_DAO = CSPEvaluatorDAO()


# CSP Evaluator
@ns.route('')
class CSPEvaluatorList(Resource):
    """Shows a list of all CSPEvaluator data and lets you POST to add new data"""

    @ns.doc('List of all CSP data')
    @ns.marshal_list_with(CSPEvaluator)
    def get(self):
        """Shows CSPEvaluator data"""
        return CSPEvaluator_DAO.get()

    @ns.doc('Create CSP data')
    @ns.expect(CSPEvaluator)
    @ns.marshal_with(CSPEvaluator_returnPost)
    def post(self):
        """Create CSPEvaluator data"""
        return CSPEvaluator_DAO.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'CSPEvaluator not found')
@ns.param('id', 'CSPEvaluator id for unique identifier')
class single_CSPEvaluatorList(Resource):
    """Show a single CSPEvaluator data"""

    @ns.doc('Get single CSPEvaluator data')
    @ns.marshal_with(CSPEvaluator)
    def get(self, id):
        """Fetch a given resource"""
        return CSPEvaluator_DAO.get(id, Type=True)
