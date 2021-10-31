from flask import (
    Flask, g, jsonify
)
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
from models.BWASP import domain as domainModel
from sqlalchemy import func

ns = Namespace('api/attackVector', description='attackVector operations')

AttackVector = ns.model('AttackVector', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'UUID': fields.Integer(required=True, description='The task unique identifier'),
    'attackVector': fields.String(required=True, description='The task details'),
    'typicalServerity': fields.String(required=True, description='The task details'),
    'description': fields.String(required=True, description='The task details')
})

AttackVector_Count = ns.model('AttackVector_Count', {
    'counting': fields.Integer(readonly=True, description='The task count')
})

class AttackVectorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.AttackVectors = 0

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            AttackVector = g.BWASP_DBObj.query(attackVectorModel).all()
            print(len(AttackVector))
            return AttackVector
        elif Type is not False and id > 0:
            AttackVector = g.BWASP_DBObj.query(attackVectorModel).filter(attackVectorModel.id == id).all()
            return AttackVector
        else:
            ns.abort(404, f"Port {id} doesn't exist")

    def count(self):
        self.counter = int(g.BWASP_DBObj.query(attackVectorModel).count())
        print(self.counter)
        return self.counter

    def retCountbyData(self, start, counting):
        self.AttackVectors = g.BWASP_DBObj.query(attackVectorModel).filter(attackVectorModel.id >= start).limit(counting).all()
        return self.AttackVectors

    def create(self, data):
        AttackVector = data
        g.BWASP_DBObj.add(
            attackVectorModel(UUID=AttackVector["UUID"],
                              attackVector=AttackVector["attackVector"],
                              typicalServerity=AttackVector["typicalServerity"],
                              description=AttackVector["description"]
                              )
        )
        g.BWASP_DBObj.commit()
        return AttackVector

AttackVector_DAO = AttackVectorDAO()


# AttackVector
@ns.route('')
class attackVectorList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ns.doc('list_attackVector')
    @ns.marshal_list_with(AttackVector)
    def get(self):
        """List all tasks"""
        return AttackVector_DAO.get()

    @ns.doc('create_attackVector')
    @ns.expect(AttackVector)
    @ns.marshal_with(AttackVector, code=201)
    def post(self):
        """Create a new task"""
        return AttackVector_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'attackVector not found')
@ns.param('id', 'The task identifier')
class attackVector(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_attackVector')
    @ns.marshal_with(AttackVector)
    def get(self, id):
        """Fetch a given resource"""
        return AttackVector_DAO.get(id, Type=True)


@ns.route('/<string:start>-<string:counting>')
@ns.response(404, 'attackVector not found')
@ns.param('start', 'The task start')
@ns.param('counting', 'The task counting')
class attackVectorData(Resource):
    """Show a attackVector Count data"""

    @ns.doc('get attackVector counting data')
    @ns.marshal_with(AttackVector)
    def get(self, start, counting):
        """Fetch a given resource"""
        return AttackVector_DAO.retCountbyData(start, counting)


@ns.route('/count')
class automation_packetList(Resource):
    """Shows a count of all attackVector data list"""

    @ns.doc('count of attackVector list')
    @ns.marshal_list_with(AttackVector_Count)
    def get(self):
        """Count of list attackVector data"""
        return {"counting": AttackVector_DAO.count()}
