from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api_returnObj import Return_object
from models.BWASP.CSPEVALUATOR import CSPEvaluator as CSPEvaluatorModel

ns = Namespace('api/cspevaluator', description='csp evaluator operations')

csp_evaluator = ns.model('CSP Evaluator model', {
    'id': fields.Integer(readonly=True, description='CspEvaluator id for unique identifier'),
    'header': fields.String(required=True, description='Content-Security Policy in HTTP header')
})

csp_evaluator_return_post = ns.model('CSP Evaluator Return Post Message', {
    "message": fields.String(readonly=True, description='message of return data')
})


class Csp_evaluator_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_return_row_count(self):
        self.counter = g.bwasp_db_obj.query(CSPEvaluatorModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(CSPEvaluatorModel).all()
            return self.selectData

        if Type is not False and self.get_return_row_count() >= id > 0:
            self.selectData = g.bwasp_db_obj.query(CSPEvaluatorModel).filter(CSPEvaluatorModel.id == id).all()
            return self.selectData

        ns.abort(404, f"CSPEvaluator data {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        CSPEvaluatorModel(
                            header=json.dumps(self.insertData[ListOfData]["header"])
                        )
                    )
                    g.bwasp_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_csp_evaluator = Csp_evaluator_data_access_object()


# CSP Evaluator
@ns.route('')
class Csp_evaluator_list(Resource):
    """Shows a list of all CSPEvaluator data and lets you POST to add new data"""

    @ns.doc('List of all CSP data')
    @ns.marshal_list_with(csp_evaluator)
    def get(self):
        """Shows CSPEvaluator data"""
        return data_access_object_for_csp_evaluator.get(id=None, Type=False)

    @ns.doc('Create CSP data')
    @ns.expect(csp_evaluator)
    @ns.marshal_with(csp_evaluator_return_post)
    def post(self):
        """Create CSPEvaluator data"""
        return data_access_object_for_csp_evaluator.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'CSPEvaluator not found')
@ns.param('id', 'CSPEvaluator id for unique identifier')
class Single_csp_evaluator_list(Resource):
    """Show a single CSPEvaluator data"""

    @ns.doc('Get single CSPEvaluator data')
    @ns.marshal_list_with(csp_evaluator)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_csp_evaluator.get(id=id, Type=True)
