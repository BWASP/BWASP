from flask import g
from flask_restx import Resource, fields, Namespace
from .api_returnObj import Return_object
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP.BWASP import domain as domainModel
# from models.DOMAIN import domain as domainModel

ns = Namespace('api/domain', description='domain operations')

domain = ns.model('domain model', {
    'id': fields.Integer(readonly=True, description='cve id for unique identifier'),
    'related_Packet': fields.Integer(required=True, description='The unique identifier based on packet id'),
    'URL': fields.String(required=True, description='target URL'),
    'URI': fields.String(required=True, description='target URI'),
    'action_URL': fields.Raw(required=True, description='target action URL'),
    'action_URL_Type': fields.Raw(required=True, description='target action URL'),
    'params': fields.Raw(required=True, description='target URL parameter'),
    'comment': fields.String(required=True, description='target Web page HTML comment'),
    'attackVector': fields.Raw(required=True, description='Attack vector about CVE, Analysis data'),
    'impactRate': fields.Integer(required=True, description='target attack vector Typical Serverity'),
    'description': fields.String(required=True, description='attack vector description'),
    'Details': fields.Raw(required=True, description='attack vector details')
})

domain_return_post_method = ns.model('domain return post method', {
    "message": fields.String(readonly=True, description='message of return data')
})

domain_count = ns.model('domain count', {
    'count': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


class Domain_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_return_row_count(self):
        self.counter = g.bwasp_db_obj.query(domainModel).count()
        return {"count": self.counter}

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(domainModel).all()
            return self.selectData

        if Type is not False and self.get_return_row_count()["count"] >= id > 0:
            self.selectData = g.bwasp_db_obj.query(domainModel).filter(domainModel.id == id).all()
            return self.selectData

        ns.abort(404, f"domain {id} doesn't exist")

    def get_return_data_for_pagination(self, start=None, counting=None):
        self.selectData = g.bwasp_db_obj.query(domainModel).filter(domainModel.id >= start).limit(counting).all()
        return self.selectData

    def create(self, data):
        if str(type(data)) == "<class 'list '>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        domainModel(related_Packet=int(self.insertData[ListOfData]["related_Packet"]),
                                    URL=str(self.insertData[ListOfData]["URL"]),
                                    URI=str(self.insertData[ListOfData]["URI"]),
                                    action_URL=self.insertData[ListOfData]["action_URL"],
                                    action_URL_Type=self.insertData[ListOfData]["action_URL_Type"],
                                    params=self.insertData[ListOfData]["params"],
                                    comment=str(self.insertData[ListOfData]["comment"]),
                                    attackVector=self.insertData[ListOfData]["attackVector"],
                                    impactRate=int(self.insertData[ListOfData]["impactRate"]),
                                    description=str(self.insertData[ListOfData]["description"]),
                                    Details=self.insertData[ListOfData]["Details"]
                                    )
                    )
                    g.bwasp_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)


data_access_object_for_domain = Domain_data_access_object()


# domain
@ns.route('')
class Domain_list(Resource):
    """Shows a list of all domain data, and lets you POST to add new data"""

    @ns.doc('List of all domain data')
    @ns.marshal_list_with(domain)
    def get(self):
        """Shows domain data"""
        return data_access_object_for_domain.get(id=None, Type=False)

    @ns.doc('Create domain data')
    @ns.expect(domain)
    @ns.marshal_with(domain_return_post_method)
    def post(self):
        """Create domain data"""
        return data_access_object_for_domain.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'domain not found')
@ns.param('id', 'domain id for unique identifier')
class Single_domain_list(Resource):
    """Show a single domain data"""

    @ns.doc('Get single domain data')
    @ns.marshal_list_with(domain)
    def get(self, id):
        """Fetch a given resource"""
        return data_access_object_for_domain.get(id=id, Type=True)


@ns.route('/<int:start>/<int:counting>')
@ns.response(404, 'domain not found')
@ns.param('start', 'domain data paging start')
@ns.param('counting', 'domain data paging end')
class Paging_domain_list(Resource):
    """Show a domain data of start, counting"""

    @ns.doc('Get domain data on paging')
    @ns.marshal_list_with(domain)
    def get(self, start, counting):
        """Fetch a given resource"""
        return data_access_object_for_domain.get_return_data_for_pagination(start=start, counting=counting)


@ns.route('/count')
class Count_domain_list(Resource):
    """Show count of all domain data"""

    @ns.doc('Get count of all domain data')
    @ns.marshal_with(domain_count)
    def get(self):
        """Fetch a given resource"""
        return data_access_object_for_domain.get_return_row_count()
        # TODO: Return Type
