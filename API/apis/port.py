from flask import g
from flask_restx import Resource, fields, Namespace
from .api_returnObj import ReturnObject
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import ports as portsModel

ns = Namespace('api/ports', description='ports operations')

ports = ns.model('Ports', {
    'id': fields.Integer(readonly=True, description='Ports id for unique identifier'),
    'service': fields.String(required=True, description='Service information in server port'),
    'target': fields.String(required=True, description='target server'),
    'port': fields.String(required=True, description='target port'),
    'result': fields.String(required=True, description='target port scanning result')
})

ports_returnPost = ns.model('ports_returnPost', {
    "message": fields.String(readonly=True, description='message of return data')
})

ports_RowCount = ns.model('ports_RowCount', {
    'RowCount': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


class PortsDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_retRowCount(self):
        self.counter = g.BWASP_DBObj.query(portsModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.BWASP_DBObj.query(portsModel).all()
            return self.selectData

        if Type is not False and id > 0:
            self.selectData = g.BWASP_DBObj.query(portsModel).filter(portsModel.id == id).all()
            return self.selectData

        ns.abort(404, f"Port {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        portsModel(service=str(self.insertData[ListOfData]["service"]),
                                   target=str(self.insertData[ListOfData]["target"]),
                                   port=str(self.insertData[ListOfData]["port"]),
                                   result=str(self.insertData[ListOfData]["result"])
                                   )
                    )
                    g.BWASP_DBObj.commit()
                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)


Ports_DAO = PortsDAO()


# ports
@ns.route('')
class PortsList(Resource):
    """Shows a list of all Ports data, and lets you POST to add new data"""

    @ns.doc('List of all ports data')
    @ns.marshal_list_with(ports)
    def get(self):
        """Shows Ports data"""
        return Ports_DAO.get()

    @ns.doc('Create Ports scanning result')
    @ns.expect(ports)
    @ns.marshal_with(ports_returnPost)
    # @ns.marshal_with(ports, code=201)
    def post(self):
        """Create Ports scanning result"""
        return Ports_DAO.create(ns.payload)
        # return Ports_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'ports not found')
@ns.param('id', 'Ports id for unique identifier')
class single_PortsList(Resource):
    """Show a single Ports item"""

    @ns.doc('Get single Ports')
    @ns.marshal_with(ports)
    def get(self, id):
        """Fetch a given resource"""
        return Ports_DAO.get(id, Type=True)


@ns.route('/count')
class count_PortsList(Resource):
    """Show count of all ports data"""

    @ns.doc('Get count of all ports data')
    @ns.marshal_with(ports_RowCount)
    def get(self):
        """Fetch a given resource"""
        return {"RowCount": Ports_DAO.get_retRowCount()}
        # TODO: Return Type
