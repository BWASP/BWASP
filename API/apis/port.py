from flask import g
from flask_restx import Resource, fields, Namespace
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


class PortsDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
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
                        portsModel(service=self.insertData[ListOfData]["service"],
                                   target=self.insertData[ListOfData]["target"],
                                   port=self.insertData[ListOfData]["port"],
                                   result=self.insertData[ListOfData]["result"]
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
                    portsModel(service=self.insertData["service"],
                               target=self.insertData["target"],
                               port=self.insertData["port"],
                               result=self.insertData["result"]
                               )
                )
                g.BWASP_DBObj.commit()
                return self.insertData
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData


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
    @ns.marshal_with(ports, code=201)
    def post(self):
        """Create Ports scanning result"""
        return Ports_DAO.create(ns.payload), 201


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
