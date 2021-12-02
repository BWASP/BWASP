from flask import g
from flask_restx import Resource, fields, Namespace
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api_returnObj import Return_object

from models.BWASP import ports as portsModel
# from models.PORTS import ports as portsModel


ns = Namespace('api/ports', description='ports operations')

ports = ns.model('Ports', {
    'id': fields.Integer(readonly=True, description='Ports id for unique identifier'),
    'service': fields.String(required=True, description='Service information in server port'),
    'target': fields.String(required=True, description='target server'),
    'port': fields.String(required=True, description='target port'),
    'result': fields.String(required=True, description='target port scanning result')
})

ports_return_post_method = ns.model('Ports Return Post Message', {
    "message": fields.String(readonly=True, description='message of return data')
})

ports_row_count = ns.model('Ports row count', {
    'count': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


class Ports_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_return_row_count(self):
        self.counter = g.bwasp_db_obj.query(portsModel).count()
        return {"count": self.counter}

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(portsModel).all()
            return self.selectData

        if Type is not False and self.get_return_row_count()["count"] >= id > 0:
            self.selectData = g.bwasp_db_obj.query(portsModel).filter(portsModel.id == id).all()
            return self.selectData

        ns.abort(404, f"Port {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        portsModel(service=self.insertData[ListOfData]["service"],
                                   target=self.insertData[ListOfData]["target"],
                                   port=self.insertData[ListOfData]["port"],
                                   result=self.insertData[ListOfData]["result"]
                                   )
                    )
                    g.bwasp_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_ports = Ports_data_access_object()


# ports
@ns.route('')
class Ports_list(Resource):
    """Shows a list of all Ports data, and lets you POST to add new data"""

    @ns.doc('List of all ports data')
    @ns.marshal_list_with(ports)
    def get(self):
        """Shows Ports data"""
        return data_access_object_for_ports.get(id=None, Type=False)

    @ns.doc('Create Ports scanning result')
    @ns.expect(ports)
    @ns.marshal_with(ports_return_post_method)
    def post(self):
        """Create Ports scanning result"""
        return data_access_object_for_ports.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'ports not found')
@ns.param('id', 'Ports id for unique identifier')
class Single_Ports_list(Resource):
    """Show a single Ports item"""

    @ns.doc('Get single Ports')
    @ns.marshal_list_with(ports)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_ports.get(id, Type=True)


@ns.route('/count')
class Count_Ports_list(Resource):
    """Show count of all ports data"""

    @ns.doc('Get count of all ports data')
    @ns.marshal_with(ports_row_count)
    def get(self):
        """Fetch a given resource"""
        return data_access_object_for_ports.get_return_row_count()
        # TODO: Return Type
