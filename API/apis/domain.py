from flask import g
from flask_restx import Resource, fields, Namespace
from models.BWASP import domain as domainModel

ns = Namespace('api/domain', description='domain operations')

domain = ns.model('Domain', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'relatePacket': fields.Integer(required=True, description='The task unique identifier'),
    'URL': fields.String(required=True, description='The task details'),
    'URI': fields.String(required=True, description='The task details'),
    'params': fields.String(required=True, description='The task details'),
    'cookie': fields.String(required=True, description='The task details'),
    'comment': fields.String(required=True, description='The task details')
})

class DomainDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.domains = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            domain = g.BWASP_DBObj.query(domainModel).all()
            return domain
        elif Type is not False and id > 0:
            domain = g.BWASP_DBObj.query(domainModel).filter(domainModel.id == id).all()
            return domain
        else:
            ns.abort(404, f"domain {id} doesn't exist")

    def create(self, data):
        domain = data
        print(domain)
        g.BWASP_DBObj.add(
            domainModel(relatePacket=domain["relatePacket"],
                        URL=domain["URL"],
                        URI=domain["URI"],
                        params=domain["params"],
                        cookie=domain["cookie"],
                        comment=domain["comment"]
                        )
        )
        g.BWASP_DBObj.commit()
        return domain

Domain_DAO = DomainDAO()

# Domain
@ns.route('')
class domainList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ns.doc('list_domain')
    @ns.marshal_list_with(domain)
    def get(self):
        """List all tasks"""
        return Domain_DAO.get()

    @ns.doc('create_domain')
    @ns.expect(domain)
    @ns.marshal_with(domain, code=201)
    def post(self):
        """Create a new task"""
        return Domain_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'domain not found')
@ns.param('id', 'The domain identifier')
class Domain(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_domain')
    @ns.marshal_with(domain)
    def get(self, id):
        """Fetch a given resource"""
        return Domain_DAO.get(id, Type=True)
