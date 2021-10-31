from flask import g
from flask_restx import Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix
from models.CVE import (
    cve as cveModel
)

ns = Namespace('api/cve/search', description='cve info operations')

cveinfo = ns.model('Cveinfo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'year': fields.String(required=True, description='The task details'),
    'description': fields.String(required=True, description='The task details'),
})

class CVEInfoDAO(object):
    def __init__(self):
        self.counter = 0
        self.cveInfo = list()

    def Search_get(self, framework="", version=""):
        if framework == "" or version == "":
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")

        self.counter = g.CVE_DBObj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).count()
        if self.counter == 0:
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")
        else:
            self.cveInfo = g.CVE_DBObj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).order_by(
                cveModel.year.desc()).all()

        return self.cveInfo

CVEInfo_DAO = CVEInfoDAO()



# CVE
@ns.route('/<string:framework>/<string:version>')
class attackVectorList(Resource):
    """Shows a list of all cve"""

    @ns.doc('list_cveInfo')
    @ns.marshal_list_with(cveinfo)
    def get(self, framework, version):
        """List all tasks"""
        return CVEInfo_DAO.Search_get(framework, version)
