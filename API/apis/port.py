from flask import g
from flask_restx import Resource, fields, Namespace
from models.BWASP import ports as portsModel

ns = Namespace('api/ports', description='ports operations')


ports = ns.model('Ports', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'service': fields.String(required=True, description='The task details'),
    'target': fields.String(required=True, description='The task details'),
    'port': fields.String(required=True, description='The task details'),
    'result': fields.String(required=True, description='The task details')
})

class PortsDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.Ports = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            ports = g.BWASP_DBObj.query(portsModel).all()
            print(len(ports))
            return ports
        elif Type is not False and id > 0:
            ports = g.BWASP_DBObj.query(portsModel).filter(portsModel.id == id).all()
            return ports
        else:
            ns.abort(404, f"Port {id} doesn't exist")

    def create(self, data):
        ports = data
        g.BWASP_DBObj.add(
            portsModel(service=ports["service"],
                       target=ports["target"],
                       port=ports["port"],
                       result=ports["result"]
                       )
        )
        g.BWASP_DBObj.commit()
        return ports

Ports_DAO = PortsDAO()


# ports
@ns.route('')
class porttList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ns.doc('list_ports')
    @ns.marshal_list_with(ports)
    def get(self):
        """List all tasks"""
        return Ports_DAO.get()

    @ns.doc('create_packet')
    @ns.expect(ports)
    @ns.marshal_with(ports, code=201)
    def post(self):
        """Create a new task"""
        return Ports_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'ports not found')
@ns.param('id', 'The task identifier')
class Ports(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_ports')
    @ns.marshal_with(ports)
    def get(self, id):
        """Fetch a given resource"""
        return Ports_DAO.get(id, Type=True)
