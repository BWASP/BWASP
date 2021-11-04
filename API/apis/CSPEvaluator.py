from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import CSPEvaluator as CSPEvaluatorModel

ns = Namespace('api/cspevaluator', description='csp evaluator operations')

csp_evaluator = ns.model('CspEvaluator', {
    'id': fields.Integer(readonly=True, description='CspEvaluator id for unique identifier'),
    'header': fields.String(required=True, description='Content-Security Policy in HTTP header')
})


class CSPEvaluatorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            self.selectData = g.BWASP_DBObj.query(CSPEvaluatorModel).all()
            return self.selectData

        if Type is not False and id > 0:
            self.selectData = g.BWASP_DBObj.query(CSPEvaluatorModel).filter(CSPEvaluatorModel.id == id).all()
            return self.selectData

        ns.abort(404, f"CSP data {id} doesn't exist")

    def create(self, data):
        if str(str(type(data))) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        CSPEvaluatorModel(
                                          header=str(self.insertData[ListOfData]["header"])
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
                    CSPEvaluatorModel(header=str(self.insertData["header"]))
                )
                g.BWASP_DBObj.commit()
                return self.insertData
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData


CSPEvaluator_DAO = CSPEvaluatorDAO()


# CSP Evaluator
@ns.route('')
class CSPEvaluatorList(Resource):
    """Shows a list of all CSPEvaluator data and lets you POST to add new data"""

    @ns.doc('List of all CSP data')
    @ns.marshal_list_with(csp_evaluator)
    def get(self):
        """Shows CSPEvaluator data"""
        return CSPEvaluator_DAO.get()

    @ns.doc('Create CSP data')
    @ns.expect(csp_evaluator)
    @ns.marshal_with(csp_evaluator, code=201)
    def post(self):
        """Create CSPEvaluator data"""
        return CSPEvaluator_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'CSPEvaluator not found')
@ns.param('id', 'CSPEvaluator id for unique identifier')
class single_CSPEvaluatorList(Resource):
    """Show a single CSPEvaluator data"""

    @ns.doc('Get single CSPEvaluator data')
    @ns.marshal_with(csp_evaluator)
    def get(self, id):
        """Fetch a given resource"""
        return CSPEvaluator_DAO.get(id, Type=True)
