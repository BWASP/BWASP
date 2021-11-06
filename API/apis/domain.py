from flask import g
from flask_restx import Resource, fields, Namespace, model
from .api_returnObj import ReturnObject
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import domain as domainModel

ns = Namespace('api/domain', description='domain operations')

domain = ns.model('Domain', {
    'id': fields.Integer(readonly=True, description='cve id for unique identifier'),
    'related_Packet': fields.Integer(required=True, description='The unique identifier based on packet id'),
    'URL': fields.String(required=True, description='target URL'),
    'URI': fields.String(required=True, description='target URI'),
    'action_URL': fields.String(required=True, description='target action URL'),
    'action_URL_Type': fields.String(required=True, description='target action URL'),
    'params': fields.String(required=True, description='target URL parameter'),
    'comment': fields.String(required=True, description='target Web page HTML comment'),
    'attackVector': fields.String(required=True, description='Attack vector about CVE, Analysis data'),
    'typicalServerity': fields.Integer(required=True, description='target attack vector Typical Serverity'),
    'description': fields.String(required=True, description='attack vector description'),
    'Details': fields.String(required=True, description='attack vector details')
})

domain_returnPost = ns.model('domain_returnPost', {
    "message": fields.String(readonly=True, description='message of return data')
})

domain_RowCount = ns.model('domain_RowCount', {
    'RowCount': fields.Integer(readonly=True, description='Count of all CspEvaluator id data')
})


class DomainDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get_retRowCount(self):
        self.counter = g.BWASP_DBObj.query(domainModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.BWASP_DBObj.query(domainModel).all()
            return self.selectData

        if Type is not False and self.get_retRowCount() >= id > 0:
            self.selectData = g.BWASP_DBObj.query(domainModel).filter(domainModel.id == id).all()
            return self.selectData

        ns.abort(404, f"domain {id} doesn't exist")

    def get_retRowData_for_Pagination(self, start, end):
        self.selectData = g.BWASP_DBObj.query(domainModel).filter(domainModel.id >= start).limit(end).all()
        return self.selectData

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        domainModel(related_Packet=int(self.insertData[ListOfData]["related_Packet"]),
                                    URL=str(self.insertData[ListOfData]["URL"]),
                                    URI=str(self.insertData[ListOfData]["URI"]),
                                    action_URL=str(self.insertData[ListOfData]["action_URL"]),
                                    action_URL_Type=str(self.insertData[ListOfData]["action_URL_Type"]),
                                    params=str(self.insertData[ListOfData]["params"]),
                                    comment=str(self.insertData[ListOfData]["comment"]),
                                    attackVector=str(self.insertData[ListOfData]["attackVector"]),
                                    typicalServerity=int(self.insertData[ListOfData]["typicalServerity"]),
                                    description=str(self.insertData[ListOfData]["description"]),
                                    Details=str(self.insertData[ListOfData]["Details"])
                                    )
                    )
                    g.BWASP_DBObj.commit()
                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)


Domain_DAO = DomainDAO()


# Domain
@ns.route('')
class domainList(Resource):
    """Shows a list of all domain data, and lets you POST to add new data"""

    @ns.doc('List of all domain data')
    @ns.marshal_list_with(domain)
    def get(self):
        """Shows domain data"""
        return Domain_DAO.get()

    @ns.doc('Create domain data')
    @ns.expect(domain)
    @ns.marshal_with(domain_returnPost)
    # @ns.marshal_with(domain, code=201)
    def post(self):
        """Create domain data"""
        return Domain_DAO.create(ns.payload)
        # return Domain_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'domain not found')
@ns.param('id', 'domain id for unique identifier')
class single_DomainList(Resource):
    """Show a single domain data"""

    @ns.doc('Get single domain data')
    @ns.marshal_with(domain)
    def get(self, id):
        """Fetch a given resource"""
        return Domain_DAO.get(id, Type=True)


@ns.route('/<int:start>/<int:end>')
@ns.response(404, 'domain not found')
@ns.param('start', 'domain data paging start')
@ns.param('end', 'domain data paging end')
class paging_DomainList(Resource):
    """Show a domain data of start, end"""

    @ns.doc('Get domain data on paging')
    @ns.marshal_list_with(domain)
    def get(self, start, end):
        """Fetch a given resource"""
        return Domain_DAO.get_retRowData_for_Pagination(start, end)


@ns.route('/count')
class count_CSPEvaluatorList(Resource):
    """Show count of all domain data"""

    @ns.doc('Get count of all domain data')
    @ns.marshal_with(domain_RowCount)
    def get(self):
        """Fetch a given resource"""
        return {"RowCount": Domain_DAO.get_retRowCount()}
        # TODO: Return Type
