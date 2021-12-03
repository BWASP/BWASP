from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
# from .api_custom_fields import StringToJSON
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api_returnObj import Return_object

from models.BWASP.BWASP import packet as packetsModel
# from models.PACKET import packet as packetModel

ns = Namespace('api/packet', description='packet operations')

packet = ns.model('Packet model', {
    'id': fields.Integer(readonly=True, description='packet id for unique identifier'),
    'category': fields.Integer(readonly=True, description='packet classification'),
    'statusCode': fields.Integer(required=True, description='status code'),
    'requestType': fields.String(required=True, description='request type'),
    'requestJson': fields.Raw(required=True, description='request data'),
    'responseHeader': fields.Raw(required=True, description='response header'),
    'responseBody': fields.String(required=True, description='response body')
})

packet_return_post_method = ns.model('Packet Return Post Message', {
    "message": fields.String(readonly=True, description='message of return data')
})

packet_index = ns.model('Packet Index', {
    "id": fields.String(readonly=True, description='packet id list for classification')
})

packet_count = ns.model('Packet Row Count', {
    'count': fields.Integer(readonly=True, description='Count of all packets id data')
})


class Packet_data_access_object(object):
    def __init__(self):
        self.DefineAutomation = 0
        self.DefineManual = 1

        self.Automation_Counter = 0
        self.Manual_Counter = 0

        self.selectData = ""
        self.insertData = ""

    def get_row_id_invalid_check(self, id=None, Type=None):
        if id is not None and Type is True:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation, packetsModel.id == id).count()

        if id is not None and Type is False:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineManual, packetsModel.id == id).count()

        return True if self.selectData != 0 else False

    # id count in table of packets
    def get_return_row_count(self, Type=None):
        self.Automation_Counter = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).count()
        self.Manual_Counter = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineManual).count()

        if Type is True:
            return {"count": int(self.Automation_Counter)}

        if Type is False:
            return {"count": int(self.Manual_Counter)}

    def get_all_packets(self, id):
        self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.id == id).all()

        if self.selectData == "":
            ns.abort(404, f"packet {id} doesn't exist")

        return self.selectData

    def get_automation(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).all()
            return self.selectData

        if Type is not False and self.get_row_id_invalid_check(id, Type=True) and id > 0:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineAutomation).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def get_manual(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.category == self.DefineManual).all()
            return self.selectData

        if Type is not False and self.get_row_id_invalid_check(id, Type=False) and id > 0:
            self.selectData = g.bwasp_db_obj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineManual).first()
            return self.selectData

        ns.abort(404, f"packet {id} doesn't exist")

    def get_automation_index(self):
        self.selectData = g.bwasp_db_obj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all()
        retIndex = list()

        for idx in range(len(self.selectData)):
            retIndex.append(self.selectData[idx].id)

        return {"id": retIndex}  # automaton id of packet list

    def get_manual_index(self):
        self.selectData = g.bwasp_db_obj.query(packetsModel.id).filter(packetsModel.category == self.DefineManual).all()
        retIndex = list()

        for idx in range(len(self.selectData)):
            retIndex.append(self.selectData[idx].id)

        return {"id": retIndex}  # manual id of packet list

    def create_automation(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        packetsModel(category=0,
                                     statusCode=int(self.insertData[ListOfData]['statusCode']),
                                     requestType=self.insertData[ListOfData]['requestType'],
                                     requestJson=self.insertData[ListOfData]['requestJson'],
                                     responseHeader=self.insertData[ListOfData]['responseHeader'],
                                     responseBody=self.insertData[ListOfData]['responseBody']
                                     )
                    )
                    g.bwasp_db_obj.commit()
                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)

    def create_manual(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        packetsModel(category=1,
                                     statusCode=int(self.insertData[ListOfData]['statusCode']),
                                     requestType=self.insertData[ListOfData]['requestType'],
                                     requestJson=self.insertData[ListOfData]['requestJson'],
                                     responseHeader=self.insertData[ListOfData]['responseHeader'],
                                     responseBody=self.insertData[ListOfData]['responseBody']
                                     )
                    )
                    g.bwasp_db_obj.commit()
                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_packet = Packet_data_access_object()


# Packets
@ns.route('/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class All_packets_list(Resource):
    """Shows a list of all packets"""

    @ns.doc("List of all packets")
    @ns.marshal_list_with(packet)
    def get(self, id):
        return data_access_object_for_packet.get_all_packets(id=id)


@ns.route('/automation')
class Automation_packet_list(Resource):
    """Shows a list of all automation packets, and lets you POST to add new data"""

    @ns.doc('List of all automation packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows automation packets"""
        return data_access_object_for_packet.get_automation(id=None, Type=False)

    @ns.doc('Create automation packet')
    @ns.expect(packet)
    @ns.marshal_with(packet_return_post_method)
    def post(self):
        """Create automation packet"""
        return data_access_object_for_packet.create_automation(ns.payload)


@ns.route('/manual')
class Manual_packet_list(Resource):
    """Shows a list of all manual packets, and lets you POST to add new data"""

    @ns.doc('List of all manual packets')
    @ns.marshal_list_with(packet)
    def get(self):
        """Shows manual packets"""
        return data_access_object_for_packet.get_manual(id=None, Type=False)

    @ns.doc('Create manual packet')
    @ns.expect(packet)
    @ns.marshal_with(packet_return_post_method)
    def post(self):
        """Create manual packet"""
        return data_access_object_for_packet.create_manual(ns.payload)


@ns.route('/automation/index')
class Automation_packet_index(Resource):
    """Shows a list of all automation packet id"""

    @ns.doc('List of all automation packet id')
    @ns.marshal_with(packet_index)
    def get(self):
        """Shows automation packets id list"""
        return data_access_object_for_packet.get_automation_index()


@ns.route('/manual/index')
class Manual_packet_index(Resource):
    """Shows a list of all manual packet id"""

    @ns.doc('List of all manual packet id')
    @ns.marshal_with(packet_index)
    def get(self):
        """Shows manual packets id list"""
        return data_access_object_for_packet.get_manual_index()


@ns.route('/automation/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class Automation_single_packet_list(Resource):
    """Show a single packet data for automation"""

    @ns.doc('Get single packet data for automation')
    @ns.marshal_list_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_packet.get_automation(id=id, Type=True)


@ns.route('/manual/<int:id>')
@ns.response(404, 'packet not found')
@ns.param('id', 'Packet id for unique identifier')
class Manual_single_packet_list(Resource):
    """Show a single packet data for manual"""

    @ns.doc('Get single packet data for manual')
    @ns.marshal_list_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_packet.get_manual(id=id, Type=True)


@ns.route('/automation/count')
class Count_automation_packet_list(Resource):
    """Show count of all domain data"""

    @ns.doc('Get count of all domain data')
    @ns.marshal_with(packet_count)
    def get(self):
        """Fetch a given resource"""
        return data_access_object_for_packet.get_return_row_count(Type=True)
        # TODO: Return Type


@ns.route('/manual/count')
class Count_manual_packet_list(Resource):
    """Show count of all packet data"""

    @ns.doc('Get count of all packet data')
    @ns.marshal_with(packet_count)
    def get(self):
        """Fetch a given resource"""
        return data_access_object_for_packet.get_return_row_count(Type=False)
        # TODO: Return Type
