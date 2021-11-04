from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.BWASP import systeminfo as systeminfoModel

ns = Namespace('api/systeminfo', description='system info operations')

systeminfo = ns.model('SystemInfo', {
    'id': fields.Integer(readonly=True, description='system-info id for unique identifier'),
    'url': fields.String(required=True, description='target URL'),
    'data': fields.String(required=True, description='target system information')
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

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            self.selectData = g.BWASP_DBObj.query(systeminfoModel).all()
            return self.selectData

        if Type is not False and id > 0:
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
                                        data=str(self.insertData[ListOfData]["data"])
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
                    systeminfoModel(url=str(self.insertData["url"]),
                                    data=str(self.insertData["data"])
                                    )
                )
                g.BWASP_DBObj.commit()
                return self.insertData
            except:
                g.BWASP_DBObj.rollback()

        return self.insertData

    def update(self, data):
        try:
            self.updateData = data
            g.BWASP_DBObj.query(systeminfoModel).filter(systeminfoModel.id == int(self.updateData["id"])).update({'data': str(self.updateData["data"])})
            g.BWASP_DBObj.commit()
            return self.insertData
        except:
            g.BWASP_DBObj.rollback()

        return self.updateData


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
    @ns.marshal_with(systeminfo, code=201)
    def post(self):
        """Create system information"""
        return Systeminfo_DAO.create(ns.payload), 201

    @ns.expect(Update_SystemInfo)
    @ns.marshal_with(Update_SystemInfo)
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
