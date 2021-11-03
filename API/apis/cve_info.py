from flask import g
from flask_restx import Resource, fields, Namespace, model
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.CVE import cve as cveModel

ns = Namespace('api/cve/search', description='cve info operations')

CVEInfo = ns.model('CVEInfo', {
    'id': fields.Integer(readonly=True, description='CVE id for unique identifier'),
    'year': fields.String(required=True, description='CVE ID numbering'),
    'description': fields.String(required=True, description='CVE description'),
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
class CVEList(Resource):
    """Shows a list of cve"""

    @ns.doc('List of cve info')
    @ns.marshal_list_with(CVEInfo)
    def get(self, framework, version):
        """List a CVE info"""
        return CVEInfo_DAO.Search_get(framework, version)
