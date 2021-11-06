from flask import g
from flask_restx import Resource, fields, Namespace, model
from .api_returnObj import ReturnObject
import sys, os, json

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

packet_returnPost = ns.model('job_returnPost', {
    "message": fields.String(readonly=True, description='message of return data')
})

packetIndex = ns.model('packetIndex', {
    "id": fields.String(readonly=True, description='packet id list for classification')
})

packet_RowCount = ns.model('packet_RowCount', {
    'RowCount': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


class PacketDAO(object):
    def __init__(self):
        self.DefineAutomation = 0
        self.DefineManual = 1

        self.Automation_Counter = 0
        self.Manual_Counter = 0

        self.selectData = ""
        self.insertData = ""

    # id count in table of packets
    def get_retRowCount(self, Type=True):
        self.Automation_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).count()
        self.Manual_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).count()

        if Type is True:
            return int(self.Automation_Counter)

        if Type is False:
            return int(self.Manual_Counter)

    def get_automation(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).all()
            return self.selectData

        if Type is not False and self.get_retRowCount(Type=True) >= id > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineAutomation).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def get_manual(self, id=0, Type=False):
        if Type is False and self.get_retRowCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).all()
            return self.selectData

        if Type is not False and self.get_retRowCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineManual).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def get_automationIndex(self):
        self.selectData = g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all()
        return self.selectData  # automaton id of packet list

    def get_manualIndex(self):
        self.selectData = g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineManual).all()
        return self.selectData  # manual id of packet list

    def create_automation(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        packetsModel(category=0,
                                     statusCode=int(self.insertData[ListOfData]['statusCode']),
                                     requestType=str(self.insertData[ListOfData]['requestType']),
                                     requestJson=str(self.insertData[ListOfData]['requestJson']),
                                     responseHeader=str(self.insertData[ListOfData]['responseHeader']),
                                     responseBody=str(self.insertData[ListOfData]['responseBody'])
                                     )
                    )
                    g.BWASP_DBObj.commit()
                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)

    def create_manual(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        packetsModel(category=1,
                                     statusCode=int(self.insertData[ListOfData]['statusCode']),
                                     requestType=str(self.insertData[ListOfData]['requestType']),
                                     requestJson=str(self.insertData[ListOfData]['requestJson']),
                                     responseHeader=str(self.insertData[ListOfData]['responseHeader']),
                                     responseBody=str(self.insertData[ListOfData]['responseBody'])
                                     )
                    )
                    g.BWASP_DBObj.commit()
                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)


Packet_DAO = PacketDAO()


# Packets
@ns.route('/automation')
class automation_packetList(Resource):
    """Shows a list of all automation packets, and lets you POST to add new data"""

    @ns.doc('List of all automation packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows automation packets"""
        return Packet_DAO.get_automation()

    @ns.doc('Create automation packet')
    @ns.expect(packet)
    @ns.marshal_with(packet_returnPost)
    # @ns.marshal_with(packet, code=201)
    def post(self):
        """Create automation packet"""
        return Packet_DAO.create_automation(ns.payload)
        # return Packet_DAO.create_automation(ns.payload), 201


@ns.route('/manual')
class manual_packetList(Resource):
    """Shows a list of all manual packets, and lets you POST to add new data"""

    @ns.doc('List of all manual packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows manual packets"""
        return Packet_DAO.get_manual()

    @ns.doc('Create manual packet')
    @ns.expect(packet)
    @ns.marshal_with(packet)
    # @ns.marshal_with(packet, code=201)
    def post(self):
        """Create manual packet"""
        return Packet_DAO.create_manual(ns.payload)
        # return Packet_DAO.create_manual(ns.payload), 201


@ns.route('/automation/index')
class automation_packetIndex(Resource):
    """Shows a list of all automation packet id"""

    @ns.doc('List of all automation packet id')
    @ns.marshal_list_with(packetIndex)
    def get(self):
        """Shows automation packets id list"""
        return {"id": str(Packet_DAO.get_automationIndex()).replace("(", "").replace(",)", "")}


@ns.route('/manual/index')
class manual_packetIndex(Resource):
    """Shows a list of all manual packet id"""

    @ns.doc('List of all manual packet id')
    @ns.marshal_list_with(packetIndex)
    def get(self):
        """Shows manual packets id list"""
        return {"id": str(Packet_DAO.get_manualIndex()).replace("(", "").replace(",)", "")}


@ns.route('/automation/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class automation_single_packetList(Resource):
    """Show a single packet data for automation"""

    @ns.doc('Get single packet data for automation')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.get_automation(id, Type=True)


@ns.route('/manual/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class manual_single_packetList(Resource):
    """Show a single packet data for manual"""

    @ns.doc('Get single packet data for manual')
    @ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.get_manual(id, Type=True)


@ns.route('/automation/count')
class count_automation_packetList(Resource):
    """Show count of all domain data"""

    @ns.doc('Get count of all domain data')
    @ns.marshal_with(packet_RowCount)
    def get(self):
        """Fetch a given resource"""
        return {"RowCount": Packet_DAO.get_retRowCount(Type=True)}
        # TODO: Return Type


@ns.route('/manual/count')
class count_manual_packetList(Resource):
    """Show count of all packet data"""

    @ns.doc('Get count of all packet data')
    @ns.marshal_with(packet_RowCount)
    def get(self):
        """Fetch a given resource"""
        return {"RowCount": Packet_DAO.get_retRowCount(Type=False)}
        # TODO: Return Type
