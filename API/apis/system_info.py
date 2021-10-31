from flask import (
    Flask, g, jsonify
)
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
from models.BWASP import systeminfo as systeminfoModel
from sqlalchemy import func

ns = Namespace('api/systeminfo', description='system-info operations')

systeminfo = ns.model('Systeminfo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'url': fields.String(required=True, description='The task details'),
    'data': fields.String(required=True, description='The task details')
})

class SysteminfoDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.Systeminfos = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            systeminfo = g.BWASP_DBObj.query(systeminfoModel).all()
            print(len(systeminfo))
            return systeminfo
        elif Type is not False and id > 0:
            systeminfo = g.BWASP_DBObj.query(systeminfoModel).filter(systeminfoModel.id == id).all()
            return systeminfo
        else:
            ns.abort(404, f"System-info {id} doesn't exist")

    def create(self, data):
        systeminfo = data
        g.BWASP_DBObj.add(
            systeminfoModel(url=systeminfo["url"],
                            data=systeminfo["data"]
                            )
        )
        g.BWASP_DBObj.commit()
        return systeminfo


Systeminfo_DAO = SysteminfoDAO()

# Systeminfo
@ns.route('')
class systeminfotList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ns.doc('list_systeminfo')
    @ns.marshal_list_with(systeminfo)
    def get(self):
        """List all tasks"""
        return Systeminfo_DAO.get()

    @ns.doc('create_packet')
    @ns.expect(systeminfo)
    @ns.marshal_with(systeminfo, code=201)
    def post(self):
        """Create a new task"""
        return Systeminfo_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'systeminfo not found')
@ns.param('id', 'The task identifier')
class Systeminfo(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_packet')
    @ns.marshal_with(systeminfo)
    def get(self, id):
        """Fetch a given resource"""
        return Systeminfo_DAO.get(id, Type=True)
