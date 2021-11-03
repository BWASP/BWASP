from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import packets as packetsModel

ns = Namespace('api/packet', description='packet operations')

packet = ns.model('PacketData', {
    'id': fields.Integer(readonly=True, description='packet id for unique identifier'),
    'category': fields.Integer(readonly=True, description='packet classification'),
    'statusCode': fields.Integer(required=True, description='status code'),
    'requestType': fields.String(required=True, description='request type'),
    'requestJson': fields.String(required=True, description='request data'),
    'responseHeader': fields.String(required=True, description='response header'),
    'responseBody': fields.String(required=True, description='response body')
})

packetID = ns.model('PacketID', {
    "id": fields.String(required=True, description='packet id list for classification')
})


class PacketDAO(object):
    def __init__(self):
        self.DefineAutomation = 0
        self.DefineManual = 1
        self.Automation_Counter = 0
        self.Manual_Counter = 0

        self.selectData = ""
        self.insertData = ""

    def retPacketCount(self, Type=True):
        self.Automation_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).count()
        self.Manual_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).count()

        if Type:
            return int(self.Automation_Counter)
        else:
            return int(self.Manual_Counter)

    def automation_get(self, id=0, Type=False):
        if Type is False and self.retPacketCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).all()
            return self.selectData

        if Type is not False and self.retPacketCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineAutomation).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def manual_get(self, id=0, Type=False):
        if Type is False and self.retPacketCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).all()
            return self.selectData

        if Type is not False and self.retPacketCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineManual).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def automation_index_get(self):
        self.selectData = g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all()
        return self.selectData  # automaton id of packet list

    def manual_index_get(self):
        self.selectData = g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineManual).all()
        return self.selectData  # manual id of packet list

    def automation_create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        packetsModel(category=0,
                                     statusCode=self.insertData[ListOfData]['statusCode'],
                                     requestType=self.insertData[ListOfData]['requestType'],
                                     requestJson=self.insertData[ListOfData]['requestJson'],
                                     responseHeader=self.insertData[ListOfData]['responseHeader'],
                                     responseBody=self.insertData[ListOfData]['responseBody']
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
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData

    def manual_create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                for ListOfData in range(len(data)):
                    self.insertData = data

                    g.BWASP_DBObj.add(
                        packetsModel(category=1,
                                     statusCode=self.insertData[ListOfData]['statusCode'],
                                     requestType=self.insertData[ListOfData]['requestType'],
                                     requestJson=self.insertData[ListOfData]['requestJson'],
                                     responseHeader=self.insertData[ListOfData]['responseHeader'],
                                     responseBody=self.insertData[ListOfData]['responseBody']
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
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData


Packet_DAO = PacketDAO()


# Packets
@ns.route('/automation')
class automation_packetList(Resource):
    """Shows a list of all automation packets, and lets you POST to add new data"""

    @ns.doc('List of all automation packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows automation packets"""
        return Packet_DAO.automation_get()

    @ns.doc('Create automation packet')
    @ns.expect(packet)
    @ns.marshal_with(packet, code=201)
    def post(self):
        """Create automation packet"""
        return Packet_DAO.automation_create(ns.payload), 201


@ns.route('/manual')
class manual_packetList(Resource):
    """Shows a list of all manual packets, and lets you POST to add new data"""

    @ns.doc('List of all manual packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows manual packets"""
        return Packet_DAO.manual_get()

    @ns.doc('Create manual packet')
    @ns.expect(packet)
    @ns.marshal_with(packet, code=201)
    def post(self):
        """Create manual packet"""
        return Packet_DAO.manual_create(ns.payload), 201


@ns.route('/automation/index')
class automation_packetID(Resource):
    """Shows a list of all automation packet id"""

    @ns.doc('List of all automation packet id')
    @ns.marshal_list_with(packetID)
    def get(self):
        """Shows automation packets id list"""
        return {"id": Packet_DAO.automation_index_get()}


@ns.route('/manual/index')
class manual_packetID(Resource):
    """Shows a list of all manual packet id"""

    @ns.doc('List of all manual packet id')
    @ns.marshal_list_with(packetID)
    def get(self):
        """Shows manual packets id list"""
        return {"id": Packet_DAO.manual_index_get()}


@ns.route('/automation/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class automation_single_packetList(Resource):
    """Show a single packet data for automation"""

    @ns.doc('Get single packet data for automation')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.automation_get(id, Type=True)


@ns.route('/manual/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class manual_single_packetList(Resource):
    """Show a single packet data for manual"""

    @ns.doc('Get single packet data for manual')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.manual_get(id, Type=True)
