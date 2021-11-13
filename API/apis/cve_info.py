from flask import g
from flask_restx import (
    Resource, fields, Namespace, model
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.CVE import cve as cveModel

ns = Namespace('api/cve/search', description='cve info operations')

cve_info = ns.model('CVE information model', {
    'id': fields.Integer(readonly=True, description='CVE id for unique identifier'),
    'year': fields.String(required=True, description='CVE ID numbering'),
    'description': fields.String(required=True, description='CVE description'),
})


class Cve_information_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.cveInfo = list()

    def get_search_cve_list(self, framework=None, version=None):
        if framework is None or version is None:
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")

        self.counter = g.cve_db_obj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).count()

        if self.counter == 0:
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")
        else:
            self.cveInfo = g.cve_db_obj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).order_by(
                cveModel.year.desc()).all()

        return self.cveInfo


data_access_object_for_cve_information = Cve_information_data_access_object()


# CVE
@ns.route('/<string:framework>/<string:version>')
class Cve_list(Resource):
    """Shows a list of cve"""

    @ns.doc('List of cve info')
    @ns.marshal_list_with(cve_info)
    def get(self, framework, version):
        """List a CVE info"""
        return data_access_object_for_cve_information.get_search_cve_list(framework, version)
