from flask import g
from flask_restx import (
    Resource, fields, Namespace
)
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.CVELIST.CVELIST import cve as cveModel

ns = Namespace('api/cve/search', description='cve info operations')

cve_info = ns.model('CVE information model', {
    'id': fields.Integer(readonly=True, description='CVE id for unique identifier'),
    'year': fields.String(required=True, description='CVE ID numbering'),
    'description': fields.String(required=True, description='CVE description'),
})

cve_info_count = ns.model('CVE information model counting', {
    'count': fields.Integer(readonly=True, description='CVE list count')
})


class Cve_information_data_access_object(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.cve_list = ""
        self.limitCount = 9

    def get_search_cve_list(self, framework=None, version=None):
        if framework is None and version is None:
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")

        self.selectData = g.cve_db_obj.query(cveModel).filter(
            cveModel.description.like(f"%{framework}%")
        ) if version == "0" else g.cve_db_obj.query(cveModel).filter(
            cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")
        )

        self.counter = self.selectData.order_by(cveModel.year.desc()).limit(self.limitCount).count()

        if self.counter < 1:
            ns.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")

        self.cve_list = self.selectData.order_by(cveModel.year.desc()).limit(self.limitCount).all()
        return self.cve_list

    def get_count_of_search_cve_list(self, framework=None, version=None):
        self.selectData = g.cve_db_obj.query(cveModel).filter(
            cveModel.description.like(f"%{framework}%")
        ) if version == "0" else g.cve_db_obj.query(cveModel).filter(
            cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")
        )

        self.counter = self.selectData.order_by(cveModel.year.desc()).count()
        return {"count": int(self.counter)}


data_access_object_for_cve_information = Cve_information_data_access_object()


# CVE
@ns.route('/<string:framework>/<string:version>')
class Cve_list(Resource):
    """Shows a list of cve"""

    @ns.doc('List of cve info')
    @ns.marshal_list_with(cve_info)
    def get(self, framework, version):
        """List a CVE info"""
        return data_access_object_for_cve_information.get_search_cve_list(framework=framework, version=version)


@ns.route('/<string:framework>/<string:version>/count')
class Count_of_cve_list(Resource):
    """Shows a count of cve list"""

    @ns.doc('Count of cve info list')
    @ns.marshal_with(cve_info_count)
    def get(self, framework, version):
        """count a CVE info list"""
        return data_access_object_for_cve_information.get_count_of_search_cve_list(framework=framework, version=version)
