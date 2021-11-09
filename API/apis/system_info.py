from flask import g
from flask_restx import Resource, fields, Namespace, model
from .api_returnObj import ReturnObject
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import systeminfo as systeminfoModel

ns = Namespace('api/systeminfo', description='system info operations')

systeminfo = ns.model('SystemInfo', {
    'id': fields.Integer(readonly=True, description='system-info id for unique identifier'),
    'url': fields.String(required=True, description='target URL'),
    'data': fields.String(required=True, description='target system information')
})

systeminfo_returnPost = ns.model('systeminfo_returnPost', {
    "message": fields.String(readonly=True, description='message of return data')
})

Update_SystemInfo = ns.model('Update_SystemInfo', {
    'id': fields.Integer(required=True, description='system-info id for unique identifier'),
    'data': fields.String(required=True, description='target system information')
})


class SysteminfoDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def get_retRowCount(self):
        self.counter = g.BWASP_DBObj.query(systeminfoModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.BWASP_DBObj.query(systeminfoModel).all()
            return self.selectData

        if Type is not False and self.get_retRowCount() >= id > 0:
            self.selectData = g.BWASP_DBObj.query(systeminfoModel).filter(systeminfoModel.id == id).all()
            return self.selectData

        ns.abort(404, f"System-info {id} doesn't exist")

    def create(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.BWASP_DBObj.add(
                        systeminfoModel(url=str(self.insertData[ListOfData]["url"]),
                                        data=json.dumps(self.insertData[ListOfData]["data"])
                                        )
                    )

                return ReturnObject().Return_POST_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_POST_HTTPStatusMessage(Type=False)

    def update(self, data):
        if str(type(data)) == "<class 'list'>":
            try:
                self.updateData = data

                for ListofData in range(len(data)):
                    g.BWASP_DBObj.query(systeminfoModel).filter(
                        systeminfoModel.id == int(self.updateData[ListofData]["id"])
                    ).update(
                        {'data': json.dumps(self.updateData[ListofData]["data"])}
                    )
                    g.BWASP_DBObj.commit()

                return ReturnObject().Return_PATCH_HTTPStatusMessage(Type=True)
            except:
                g.BWASP_DBObj.rollback()

        return ReturnObject().Return_PATCH_HTTPStatusMessage(Type=False)


Systeminfo_DAO = SysteminfoDAO()


# Systeminfo
@ns.route('')
class SystemInfoList(Resource):
    """Shows a list of all system-info, and lets you POST to add new data"""

    @ns.doc('List of all system-info')
    @ns.marshal_list_with(systeminfo)
    def get(self):
        """Shows system-infos"""
        return Systeminfo_DAO.get()

    @ns.doc('Create system information')
    @ns.expect(systeminfo)
    @ns.marshal_with(systeminfo_returnPost)
    def post(self):
        """Create system information"""
        return Systeminfo_DAO.create(ns.payload)

    @ns.doc('Update system information')
    @ns.expect(Update_SystemInfo)
    @ns.marshal_with(systeminfo_returnPost)
    def patch(self):
        """Update a data given its identifier"""
        return Systeminfo_DAO.update(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'systeminfo not found')
@ns.param('id', 'system-info id for unique identifier')
class single_SystemInfoList(Resource):
    """Show a single system-info item"""

    @ns.doc('Get single system-info')
    @ns.marshal_with(systeminfo)
    def get(self, id):
        """Fetch a given resource"""
        return Systeminfo_DAO.get(id, Type=True)
