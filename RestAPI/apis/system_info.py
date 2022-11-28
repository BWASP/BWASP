from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .api_returnObj import Return_object
from models.BWASP.SYSTEMINFO import systeminfo as systeminfoModel

ns = Namespace('api/systeminfo', description='system info operations')

systeminfo = ns.model('SystemInfo', {
    'id': fields.Integer(readonly=True, description='system-info id for unique identifier'),
    'url': fields.String(required=True, description='target URL'),
    'data': fields.String(required=True, description='target system information'),
    "subDomain": fields.String(required=True, description='target sub domains')
})

systeminfo_return_post_method = ns.model('system information return post message', {
    "message": fields.String(readonly=True, description='message of return data')
})

update_systeminfo = ns.model('update in system information data', {
    'id': fields.Integer(required=True, description='system-info id for unique identifier'),
    'data': fields.String(required=True, description='target system information')
})

update_subdomain = ns.model('update in system information data', {
    'id': fields.Integer(required=True, description='system-info id for unique identifier'),
    'subDomain': fields.String(required=True, description='target sub domains')
})


class Systeminfo_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""
        self.updateData = ""

    def get_return_row_count(self):
        self.counter = g.bwasp_db_obj.query(systeminfoModel).count()
        return self.counter

    def get(self, id=None, Type=False):
        if Type is False and id is None:
            self.selectData = g.bwasp_db_obj.query(systeminfoModel).all()
            return self.selectData

        if Type is not False and self.get_return_row_count() >= id > 0:
            self.selectData = g.bwasp_db_obj.query(systeminfoModel).filter(systeminfoModel.id == id).all()
            return self.selectData

        ns.abort(404, f"System-info {id} doesn't exist")

    def create(self, data):
        if type(data) == list:
            try:
                self.insertData = data

                for ListOfData in range(len(data)):
                    g.bwasp_db_obj.add(
                        systeminfoModel(url=str(self.insertData[ListOfData]["url"]),
                                        data=json.dumps(self.insertData[ListOfData]["data"])
                                        )
                    )
                    g.bwasp_db_obj.commit()

                return Return_object().return_post_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_post_http_status_message(Type=False)

    def update(self, data, Type: str = 'Sub' | 'Sys'):
        if type(data) == list:
            try:
                self.updateData = data

                if Type == 'Sub':
                    for ListofData in range(len(data)):
                        g.bwasp_db_obj.query(systeminfoModel).filter(
                            systeminfoModel.id == int(self.updateData[ListofData]["id"])
                        ).update(
                            {'subDomain': json.dumps(self.updateData[ListofData]["subDomain"])}
                        )
                        g.bwasp_db_obj.commit()

                if Type == 'Sys':
                    for ListofData in range(len(data)):
                        g.bwasp_db_obj.query(systeminfoModel).filter(
                            systeminfoModel.id == int(self.updateData[ListofData]["id"])
                        ).update(
                            {'data': json.dumps(self.updateData[ListofData]["data"])}
                        )
                        g.bwasp_db_obj.commit()

                return Return_object().return_patch_http_status_message(Type=True)
            except:
                g.bwasp_db_obj.rollback()

        return Return_object().return_patch_http_status_message(Type=False)


Systeminfo_DAO = Systeminfo_data_access_object()


# Systeminfo
@ns.route('')
class SystemInfo_list(Resource):
    """Shows a list of all system-info, and lets you POST to add new data"""

    @ns.doc('List of all system-info')
    @ns.marshal_list_with(systeminfo)
    def get(self):
        """Shows system-infos"""
        return Systeminfo_DAO.get(id=None, Type=False)

    @ns.doc('Create system information')
    @ns.expect(systeminfo)
    @ns.marshal_with(systeminfo_return_post_method)
    def post(self):
        """Create system information"""
        return Systeminfo_DAO.create(ns.payload)


@ns.route('/<int:id>')
@ns.response(404, 'systeminfo not found')
@ns.param('id', 'system-info id for unique identifier')
class Single_systemInfo_list(Resource):
    """Show a single system-info item"""

    @ns.doc('Get single system-info')
    @ns.marshal_list_with(systeminfo)
    def get(self, id):
        """Fetch a given resource"""
        return Systeminfo_DAO.get(id=id, Type=True)


@ns.route('/sysinfo')
class Single_subdomain_list(Resource):
    """Show a single subdomain item"""

    @ns.doc('Update system information')
    @ns.expect(update_systeminfo)
    @ns.marshal_with(systeminfo_return_post_method)
    def patch(self):
        """Update a data given its identifier"""
        return Systeminfo_DAO.update(ns.payload, 'Sys')


@ns.route('/sub-domain')
class Single_subdomain_list(Resource):
    """Show a single subdomain item"""

    @ns.doc('Update subdomain information')
    @ns.expect(update_subdomain)
    @ns.marshal_with(systeminfo_return_post_method)
    def patch(self):
        """Update a data given its identifier"""
        return Systeminfo_DAO.update(ns.payload, 'Sub')
