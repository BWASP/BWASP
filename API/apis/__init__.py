from flask import Blueprint
from flask_restx import Api

from .packets import ns as packet_namespace
from .CSPEvaluator import ns as csp_evaluator_namespace
from .cve_info import ns as cve_info_namespace
from .domain import ns as domain_namespace
from .job import ns as job_namespace
from .port import ns as port_namespace
from .system_info import ns as system_info_namespace

NAME = 'api'
bp = Blueprint(
    NAME,
    __name__,
    url_prefix='/'
)

api = Api(
    bp,
    version='2021.10.1',
    title='BWASP API',
    description='The BoB Web Application Security Project API Server'
)

api.add_namespace(packet_namespace)
api.add_namespace(csp_evaluator_namespace)
api.add_namespace(cve_info_namespace)
api.add_namespace(domain_namespace)
api.add_namespace(job_namespace)
api.add_namespace(port_namespace)
api.add_namespace(system_info_namespace)

