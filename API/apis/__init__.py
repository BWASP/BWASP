from flask import Blueprint
from flask_restx import Api

from .packets import ns as packetNamespace
from .CSPEvaluator import ns as cspEvaluatorNamespace
from .cve_info import ns as cveInfoNamespace
from .domain import ns as domainNamespace
from .job import ns as jobNamespace
from .port import ns as portNamespace
from .system_info import ns as systemInfoNamespace

blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/'
)

api = Api(
    blueprint,
    version='2021.10.1',
    title='BWASP API',
    description='The BoB Web Application Security Project API Server'
)

api.add_namespace(packetNamespace)
api.add_namespace(cspEvaluatorNamespace)
api.add_namespace(cveInfoNamespace)
api.add_namespace(domainNamespace)
api.add_namespace(jobNamespace)
api.add_namespace(portNamespace)
api.add_namespace(systemInfoNamespace)

