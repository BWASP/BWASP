from flask import g
from flask_restx import Resource, fields, Namespace, model
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
    'params': fields.String(required=True, description='target URL parameter'),
    'comment': fields.String(required=True, description='target Web page HTML comment'),
    'attackVector': fields.String(required=True, description='Attack vector about CVE, Analysis data'),
    'typicalServerity': fields.Integer(required=True, description='target attack vector Typical Serverity'),
    'description': fields.String(required=True, description='attack vector description'),
    'Details': fields.String(required=True, description='attack vector details')
})


class DomainDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            domain = g.BWASP_DBObj.query(domainModel).all()
            return domain

        if Type is not False and id > 0:
            domain = g.BWASP_DBObj.query(domainModel).filter(domainModel.id == id).all()
            return domain

        ns.abort(404, f"domain {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data
                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        domainModel(related_Packet=self.insertData[ListOfData]["related_Packet"],
                                    URL=self.insertData[ListOfData]["URL"],
                                    URI=self.insertData[ListOfData]["URI"],
                                    action_URL=self.insertData[ListOfData]["action_URL"],
                                    params=self.insertData[ListOfData]["params"],
                                    comment=self.insertData[ListOfData]["comment"],
                                    attackVector=self.insertData[ListOfData]["attackVector"],
                                    typicalServerity=self.insertData[ListOfData]["typicalServerity"],
                                    description=self.insertData[ListOfData]["description"],
                                    Details=self.insertData[ListOfData]["Details"]
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
                    domainModel(related_Packet=self.insertData["related_Packet"],
                                URL=self.insertData["URL"],
                                URI=self.insertData["URI"],
                                action_URL=self.insertData["action_URL"],
                                params=self.insertData["params"],
                                comment=self.insertData["comment"],
                                attackVector=self.insertData["attackVector"],
                                typicalServerity=self.insertData["typicalServerity"],
                                description=self.insertData["description"],
                                Details=self.insertData["Details"]
                                )
                )
                g.BWASP_DBObj.commit()
                return self.insertData
            except:
                print("except")
                g.BWASP_DBObj.rollback()

        return self.insertData


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
    @ns.marshal_with(domain, code=201)
    def post(self):
        """Create domain data"""
        return Domain_DAO.create(ns.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'domain not found')
@ns.param('id', 'domain id for unique identifier')
class single_Domain(Resource):
    """Show a single domain data"""

    @ns.doc('Get single domain data')
    @ns.marshal_with(domain)
    def get(self, id):
        """Fetch a given resource"""
        return Domain_DAO.get(id, Type=True)
