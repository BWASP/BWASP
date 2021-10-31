from flask import g

from flask_restx import Resource, fields, Namespace
from models.BWASP import CSPEvaluator as CSPEvaluatorModel

ns = Namespace('api/csp_evaluator', description='csp_evaluator operations')

csp_evaluator = ns.model('Csp_evaluator', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'UUID': fields.Integer(required=True, description='The task unique identifier'),
    'header': fields.String(required=True, description='The task details'),
    'analysis': fields.String(required=True, description='The task details'),
    'status': fields.String(required=True, description='The task details')
})

class CSPEvaluatorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.CSPdatas = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            csp_evaluator = g.BWASP_DBObj.query(CSPEvaluatorModel).all()
            print(len(csp_evaluator))
            return csp_evaluator
        elif Type is not False and id > 0:
            csp_evaluator = g.BWASP_DBObj.query(CSPEvaluatorModel).filter(CSPEvaluatorModel.id == id).all()
            return csp_evaluator
        else:
            ns.abort(404, f"CSP data {id} doesn't exist")

    def create(self, data):
        csp_evaluator = data
        g.BWASP_DBObj.add(
            CSPEvaluatorModel(UUID=csp_evaluator["UUID"],
                              header=csp_evaluator["header"],
                              analysis=csp_evaluator["analysis"],
                              status=csp_evaluator["status"]
                              )
        )
        g.BWASP_DBObj.commit()
        return csp_evaluator

CSPEvaluator_DAO = CSPEvaluatorDAO()


# CSP Evaluator
@ns.route('')
class csp_evaluatorList(Resource):
    """Shows a list of all csp_evaluator, and lets you POST to add new tasks"""

    @ns.doc('list_csp_evaluator')
    @ns.marshal_list_with(csp_evaluator)
    def get(self):
        """List all tasks"""
        return CSPEvaluator_DAO.get()

    @ns.doc('create_csp_evaluator')
    @ns.expect(csp_evaluator)
    @ns.marshal_with(csp_evaluator, code=201)
    def post(self):
        """Create a new task"""
        return CSPEvaluator_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'csp_evaluator not found')
@ns.param('id', 'The task identifier')
class CSPEvaluator(Resource):
    """Show a single csp_evaluator item and lets you delete them"""

    @ns.doc('get_csp_evaluator')
    @ns.marshal_with(csp_evaluator)
    def get(self, id):
        """Fetch a given resource"""
        return CSPEvaluator_DAO.get(id, Type=True)
