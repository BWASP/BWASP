from flask import (
    Flask, g, jsonify
)
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy import func

from models.BWASP import packets as packetModel

ns = Namespace('api/packets', description='packet operations')

packet = ns.model('Packet', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'category': fields.Integer(readonly=True, description='the task unique identifier'),
    'statusCode': fields.Integer(required=True, description='The task details'),
    'requestType': fields.String(required=True, description='The task details'),
    'requestJson': fields.String(required=True, description='The task details'),
    'responseHeader': fields.String(required=True, description='The task details'),
    'responseBody': fields.String(required=True, description='The task details')
})

packetID = ns.model('PacketID', {
    "id": fields.String(required=True, description='The task id list')
})

class PacketDAO(object):
    def __init__(self):
        self.DefineAutomation = 0
        self.DefineManual = 1
        self.Automation_Counter = 0
        self.Manual_Counter = 0

        self.selectData = ""
        self.insertData = ""

    def retPacketTCount(self, Type=True):
        self.Automation_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).count()
        self.Manual_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).count()

        if Type:
            return int(self.Automation_Counter)
        else:
            return int(self.Manual_Counter)

    def automation_get(self, id=0, Type=False):
        if Type is False and self.retPacketTCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).all()
            return self.selectData
        elif Type is not False and self.retPacketTCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineAutomation).first()
            return self.selectData
        else:
            ns.abort(404, f"packet {id} doesn't exist")

    def manual_get(self, id=0, Type=False):
        if Type is False and self.retPacketTCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).all()
            return self.selectData
        elif Type is not False and self.retPacketTCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineManual).first()
            return self.selectData
        else:
            ns.abort(404, f"packet {id} doesn't exist")

    def automation_index_get(self):
        self.selectData = str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(
            ",)", "")
        print(self.selectData)
        return self.selectData  # automaton id of packet list

    def manual_index_get(self):
        self.selectData = str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineManual).all())).replace("(", "").replace("),", "").replace(
            ",)", "")
        print(self.selectData)
        return self.selectData  # manual id of packet list

    def automation_create(self, data):
        for dataLength in range(len(data)):
            self.insertData = data[dataLength]
            g.BWASP_DBObj.add(
                packetsModel(category=0,
                             statusCode=self.insertData['statusCode'],
                             requestType=self.insertData['requestType'],
                             requestJson=self.insertData['requestJson'],
                             responseHeader=self.insertData['responseHeader'],
                             responseBody=self.insertData['responseBody']
                             )
            )
            g.BWASP_DBObj.commit()
        return self.insertData

    def manual_create(self, data):
        self.insertData = data
        g.BWASP_DBObj.add(
            packetsModel(category=1,
                         statusCode=self.insertData['statusCode'],
                         requestType=self.insertData['requestType'],
                         requestJson=self.insertData['requestJson'],
                         responseHeader=self.insertData['responseHeader'],
                         responseBody=self.insertData['responseBody']
                         )
        )
        g.BWASP_DBObj.commit()
        return self.insertData

Packet_DAO = PacketDAO()

# Packets
@ns.route('/automation')
class automation_packetList(Resource):
    """Shows a list of all automation packets, and lets you POST to add new tasks"""

    @ns.doc('list of automation packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """List automation packets"""
        return Packet_DAO.automation_get()

    @ns.doc('create automation packet')
    @ns.expect(packet)
    @ns.marshal_with(packet, code=201)
    def post(self):
        """Create automation packet"""
        return Packet_DAO.automation_create(ns.payload), 201


@ns.route('/automation/index')
class automation_packetList(Resource):
    """Shows a list of all automation packet id"""

    @ns.doc('id list of automation packets')
    @ns.marshal_list_with(packetID)
    def get(self):
        """List manual packets id"""
        return {"id": Packet_DAO.automation_index_get()}
        # print(str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(",)", ""))
        # return {"id": str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(",)", "")}


@ns.route('/automation/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'The task identifier')
class Packet(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_packet')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.automation_get(id, Type=True)


@ns.route('/manual')
class manual_packetList(Resource):
    """Shows a list of all manual packets, and lets you POST to add new tasks"""

    @ns.doc('list of manual packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """List manual packets"""
        return Packet_DAO.manual_get()

    @ns.doc('create manual packet')
    @ns.expect(packet)
    @ns.marshal_with(packet, code=201)
    def post(self):
        """Create manual packet"""
        return Packet_DAO.manual_create(ns.payload), 201


@ns.route('/manual/index')
class automation_packetList(Resource):
    """Shows a list of all manual packet id"""

    @ns.doc('id list of manual packets')
    @ns.marshal_list_with(packetID)
    def get(self):
        """List manual packets id"""
        return {"id": Packet_DAO.manual_index_get()}


@ns.route('/manual/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'The task identifier')
class Packet(Resource):
    """Show a single packet item and lets you delete them"""

    @ns.doc('get_packet')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.manual_get(id, Type=True)
