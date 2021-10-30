from flask import (
    Flask, g, jsonify
)
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
from sqlalchemy import func
import os

# db model import
from models.BWASP import bwasp_db as BWASP_DB_Obj
from models.BWASP import (
    CSPEvaluator as CSPEvaluatorModel,
    domain as domainModel,
    job as jobModel,
    packets as packetsModel,
    ports as portsModel,
    systeminfo as systeminfoModel,
    attackVector as attackVectorModel
)
from models.CVE import cve_db as CVE_DB_Obj
from models.CVE import (
    cve as cveModel
)
from flask_cors import CORS

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, resource={r'/api/*': {"Access-Control-Allow-Origin": "*"}})
CORS(app, resource={r'/api/*': {"Access-Control-Allow-Credentials": True}})
api = Api(
    app,
    version='2021.10.1',
    title='BWASP API',
    description='The BoB Web Application Security Project API Server'
)

# config initialization
# from configs import DevelopmentsConfig, ProductionConfig
# config = DevelopmentsConfig()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
app.config["SECRET_KEY"] = os.urandom(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databases/BWASP.db"
app.config["SQLALCHEMY_BINDS"] = {
    "BWASP": f'sqlite:///{os.path.join(BASE_PATH, "databases/BWASP.db")}',
    "CVE": f'sqlite:///{os.path.join(BASE_PATH, "databases/CVE.db")}'
}
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

"""
if app.config['DEBUG']:
    config = DevelopmentsConfig()
else:
    config = ProductionConfig()
"""
# app.config.from_object(config)

# DB initialization
BWASP_DB_Obj.init_app(app)
CVE_DB_Obj.init_app(app)
app.app_context().push()


@app.before_request
def before_request():
    BWASP_DB_Obj.app = app
    CVE_DB_Obj.app = app
    BWASP_DB_Obj.create_all()
    g.BWASP_DBObj = BWASP_DB_Obj.session
    g.CVE_DBObj = CVE_DB_Obj.session


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'database'):
        g.BWASP_DBObj.close()


packet_ns = api.namespace('api/packets', description='packet operations')
domain_ns = api.namespace('api/domain', description='domain operations')
csp_evaluator_ns = api.namespace('api/csp_evaluator', description='csp_evaluator operations')
job_ns = api.namespace('api/job', description='job operations')
ports_ns = api.namespace('api/ports', description='ports operations')
systeminfo_ns = api.namespace('api/systeminfo', description='system-info operations')
cveInfo_ns = api.namespace('api/cve/search', description='cve info operations')
attackVector_ns = api.namespace('api/attackVector', description='attackVector operations')

packet = api.model('Packet', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'category': fields.Integer(readonly=True, description='the task unique identifier'),
    'statusCode': fields.Integer(required=True, description='The task details'),
    'requestType': fields.String(required=True, description='The task details'),
    'requestJson': fields.String(required=True, description='The task details'),
    'responseHeader': fields.String(required=True, description='The task details'),
    'responseBody': fields.String(required=True, description='The task details')
})

packetID = api.model('PacketID', {
    "id": fields.String(required=True, description='The task id list')
})

domain = api.model('Domain', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'relatePacket': fields.Integer(required=True, description='The task unique identifier'),
    'URL': fields.String(required=True, description='The task details'),
    'URI': fields.String(required=True, description='The task details'),
    'params': fields.String(required=True, description='The task details'),
    'cookie': fields.String(required=True, description='The task details'),
    'comment': fields.String(required=True, description='The task details')
})

csp_evaluator = api.model('Csp_evaluator', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'UUID': fields.Integer(required=True, description='The task unique identifier'),
    'header': fields.String(required=True, description='The task details'),
    'analysis': fields.String(required=True, description='The task details'),
    'status': fields.String(required=True, description='The task details')
})

job = api.model('Job', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'targetURL': fields.String(required=True, description='The task details'),
    'knownInfo': fields.String(required=True, description='The task details'),
    'recursiveLevel': fields.String(required=True, description='The task details'),
    'uriPath': fields.String(required=True, description='The task details')
})

ports = api.model('Ports', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'service': fields.String(required=True, description='The task details'),
    'target': fields.String(required=True, description='The task details'),
    'port': fields.String(required=True, description='The task details'),
    'result': fields.String(required=True, description='The task details')
})

systeminfo = api.model('Systeminfo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'url': fields.String(required=True, description='The task details'),
    'data': fields.String(required=True, description='The task details')
})

AttackVector = api.model('AttackVector', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'UUID': fields.Integer(required=True, description='The task unique identifier'),
    'attackVector': fields.String(required=True, description='The task details'),
    'typicalServerity': fields.String(required=True, description='The task details'),
    'description': fields.String(required=True, description='The task details')
})

AttackVector_Count = api.model('AttackVector_Count', {
    'counting': fields.Integer(readonly=True, description='The task count')
})

cveinfo = api.model('Cveinfo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'year': fields.String(required=True, description='The task details'),
    'description': fields.String(required=True, description='The task details'),
})


class PacketDAO(object):
    def __init__(self):
        self.DefineAutomation = 0
        self.DefineManual = 1
        self.Automation_Counter = 0
        self.Manual_Counter = 0

        self.selectData = ""
        self.insertData = ""

    def retPacketTCount(self, Type=True):
        self.Automation_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).count()
        self.Manual_Counter = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).count()

        if Type:
            return int(self.Automation_Counter)
        else:
            return int(self.Manual_Counter)

    def automation_get(self, id=0, Type=False):
        if Type is False and self.retPacketTCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineAutomation).all()
            return self.selectData
        elif Type is not False and self.retPacketTCount(Type=True) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineAutomation).first()
            return self.selectData
        else:
            api.abort(404, f"packet {id} doesn't exist")

    def manual_get(self, id=0, Type=False):
        if Type is False and self.retPacketTCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.category == self.DefineManual).all()
            return self.selectData
        elif Type is not False and self.retPacketTCount(Type=False) > 0:
            self.selectData = g.BWASP_DBObj.query(packetsModel).filter(packetsModel.id == id, packetsModel.category == self.DefineManual).first()
            return self.selectData
        else:
            api.abort(404, f"packet {id} doesn't exist")

    def automation_index_get(self):
        self.selectData = str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(
            ",)", "")
        print(self.selectData)
        return self.selectData  # automaton id of packet list

    def manual_index_get(self):
        self.selectData = str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineManual).all())).replace("(", "").replace("),", "").replace(
            ",)", "")
        print(self.selectData)
        return self.selectData  # manual id of packet list

    def automation_create(self, data):
        for dataLength in range(len(data)):
            self.insertData = data[dataLength]
            g.BWASP_DBObj.add(
                packetsModel(category=0,
                             statusCode=self.insertData['statusCode'],
                             requestType=self.insertData['requestType'],
                             requestJson=self.insertData['requestJson'],
                             responseHeader=self.insertData['responseHeader'],
                             responseBody=self.insertData['responseBody']
                             )
            )
            g.BWASP_DBObj.commit()
        return self.insertData

    def manual_create(self, data):
        self.insertData = data
        g.BWASP_DBObj.add(
            packetsModel(category=1,
                         statusCode=self.insertData['statusCode'],
                         requestType=self.insertData['requestType'],
                         requestJson=self.insertData['requestJson'],
                         responseHeader=self.insertData['responseHeader'],
                         responseBody=self.insertData['responseBody']
                         )
        )
        g.BWASP_DBObj.commit()
        return self.insertData


class DomainDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.domains = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            domain = g.BWASP_DBObj.query(domainModel).all()
            return domain
        elif Type is not False and id > 0:
            domain = g.BWASP_DBObj.query(domainModel).filter(domainModel.id == id).all()
            return domain
        else:
            api.abort(404, f"domain {id} doesn't exist")

    def create(self, data):
        domain = data
        print(domain)
        g.BWASP_DBObj.add(
            domainModel(relatePacket=domain["relatePacket"],
                        URL=domain["URL"],
                        URI=domain["URI"],
                        params=domain["params"],
                        cookie=domain["cookie"],
                        comment=domain["comment"]
                        )
        )
        g.BWASP_DBObj.commit()
        return domain


class JobDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.jobs = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            job = g.BWASP_DBObj.query(jobModel).all()
            print(len(job))
            return job
        elif Type is not False and id > 0:
            job = g.BWASP_DBObj.query(jobModel).filter(jobModel.id == id).all()
            return job
        else:
            api.abort(404, f"job {id} doesn't exist")

    def create(self, data):
        job = data
        g.BWASP_DBObj.add(
            jobModel(targetURL=job["targetURL"],
                     knownInfo=job["knownInfo"],
                     recursiveLevel=job["recursiveLevel"],
                     uriPath=job["uriPath"]
                     )
        )
        g.BWASP_DBObj.commit()
        return job


class CSPEvaluatorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.CSPdatas = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            csp_evaluator = g.BWASP_DBObj.query(CSPEvaluatorModel).all()
            print(len(csp_evaluator))
            return csp_evaluator
        elif Type is not False and id > 0:
            csp_evaluator = g.BWASP_DBObj.query(CSPEvaluatorModel).filter(CSPEvaluatorModel.id == id).all()
            return csp_evaluator
        else:
            api.abort(404, f"CSP data {id} doesn't exist")

    def create(self, data):
        csp_evaluator = data
        g.BWASP_DBObj.add(
            CSPEvaluatorModel(UUID=csp_evaluator["UUID"],
                              header=csp_evaluator["header"],
                              analysis=csp_evaluator["analysis"],
                              status=csp_evaluator["status"]
                              )
        )
        g.BWASP_DBObj.commit()
        return csp_evaluator


class PortsDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.Ports = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            ports = g.BWASP_DBObj.query(portsModel).all()
            print(len(ports))
            return ports
        elif Type is not False and id > 0:
            ports = g.BWASP_DBObj.query(portsModel).filter(portsModel.id == id).all()
            return ports
        else:
            api.abort(404, f"Port {id} doesn't exist")

    def create(self, data):
        ports = data
        g.BWASP_DBObj.add(
            portsModel(service=ports["service"],
                       target=ports["target"],
                       port=ports["port"],
                       result=ports["result"]
                       )
        )
        g.BWASP_DBObj.commit()
        return ports


class AttackVectorDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.AttackVectors = 0

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            AttackVector = g.BWASP_DBObj.query(attackVectorModel).all()
            print(len(AttackVector))
            return AttackVector
        elif Type is not False and id > 0:
            AttackVector = g.BWASP_DBObj.query(attackVectorModel).filter(attackVectorModel.id == id).all()
            return AttackVector
        else:
            api.abort(404, f"Port {id} doesn't exist")

    def count(self):
        self.counter = int(g.BWASP_DBObj.query(attackVectorModel).count())
        print(self.counter)
        return self.counter

    def retCountbyData(self, start, counting):
        self.AttackVectors = g.BWASP_DBObj.query(attackVectorModel).filter(attackVectorModel.id >= start).limit(counting).all()
        return self.AttackVectors

    def create(self, data):
        AttackVector = data
        g.BWASP_DBObj.add(
            attackVectorModel(UUID=AttackVector["UUID"],
                              attackVector=AttackVector["attackVector"],
                              typicalServerity=AttackVector["typicalServerity"],
                              description=AttackVector["description"]
                              )
        )
        g.BWASP_DBObj.commit()
        return AttackVector


class SysteminfoDAO(object):
    def __init__(self):
        self.counter = 0
        self.selectData = ""
        self.insertData = ""

        self.Systeminfos = list()

    def get(self, id=-1, Type=False):
        if Type is False and id == -1:
            systeminfo = g.BWASP_DBObj.query(systeminfoModel).all()
            print(len(systeminfo))
            return systeminfo
        elif Type is not False and id > 0:
            systeminfo = g.BWASP_DBObj.query(systeminfoModel).filter(systeminfoModel.id == id).all()
            return systeminfo
        else:
            api.abort(404, f"System-info {id} doesn't exist")

    def create(self, data):
        systeminfo = data
        g.BWASP_DBObj.add(
            systeminfoModel(url=systeminfo["url"],
                            data=systeminfo["data"]
                            )
        )
        g.BWASP_DBObj.commit()
        return systeminfo


class CVEInfoDAO(object):
    def __init__(self):
        self.counter = 0
        self.cveInfo = list()

    def Search_get(self, framework="", version=""):
        if framework == "" or version == "":
            api.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")

        self.counter = g.CVE_DBObj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).count()
        if self.counter == 0:
            api.abort(404, f"cve info doesn't exist; Your framework: {framework}, Version: {version}")
        else:
            self.cveInfo = g.CVE_DBObj.query(cveModel).filter(cveModel.description.like(f"%{framework}%"), cveModel.description.like(f"%{version}%")).order_by(
                cveModel.year.desc()).all()

        return self.cveInfo


Packet_DAO = PacketDAO()
Domain_DAO = DomainDAO()
Job_DAO = JobDAO()
Systeminfo_DAO = SysteminfoDAO()
CSPEvaluator_DAO = CSPEvaluatorDAO()
Ports_DAO = PortsDAO()
AttackVector_DAO = AttackVectorDAO()
CVEInfo_DAO = CVEInfoDAO()


# Packets
@packet_ns.route('/automation')
class automation_packetList(Resource):
    """Shows a list of all automation packets, and lets you POST to add new tasks"""

    @packet_ns.doc('list of automation packets')
    @packet_ns.marshal_list_with(packet)
    def get(self):
        """List automation packets"""
        return Packet_DAO.automation_get()

    @packet_ns.doc('create automation packet')
    @packet_ns.expect(packet)
    @packet_ns.marshal_with(packet, code=201)
    def post(self):
        """Create automation packet"""
        return Packet_DAO.automation_create(api.payload), 201


@packet_ns.route('/automation/index')
class automation_packetList(Resource):
    """Shows a list of all automation packet id"""

    @packet_ns.doc('id list of automation packets')
    @packet_ns.marshal_list_with(packetID)
    def get(self):
        """List manual packets id"""
        return {"id": Packet_DAO.automation_index_get()}
        # print(str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(",)", ""))
        # return {"id": str(list(g.BWASP_DBObj.query(packetsModel.id).filter(packetsModel.category == self.DefineAutomation).all())).replace("(", "").replace("),", "").replace(",)", "")}


@packet_ns.route('/automation/<int:id>')
@packet_ns.response(404, 'packet not found')
@packet_ns.param('id', 'The task identifier')
class Packet(Resource):
    """Show a single packet item and lets you delete them"""

    @packet_ns.doc('get_packet')
    @packet_ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.automation_get(id, Type=True)


@packet_ns.route('/manual')
class manual_packetList(Resource):
    """Shows a list of all manual packets, and lets you POST to add new tasks"""

    @packet_ns.doc('list of manual packets')
    @packet_ns.marshal_list_with(packet)
    def get(self):
        """List manual packets"""
        return Packet_DAO.manual_get()

    @packet_ns.doc('create manual packet')
    @packet_ns.expect(packet)
    @packet_ns.marshal_with(packet, code=201)
    def post(self):
        """Create manual packet"""
        return Packet_DAO.manual_create(api.payload), 201


@packet_ns.route('/manual/index')
class automation_packetList(Resource):
    """Shows a list of all manual packet id"""

    @packet_ns.doc('id list of manual packets')
    @packet_ns.marshal_list_with(packetID)
    def get(self):
        """List manual packets id"""
        return {"id": Packet_DAO.manual_index_get()}


@packet_ns.route('/manual/<int:id>')
@packet_ns.response(404, 'packet not found')
@packet_ns.param('id', 'The task identifier')
class Packet(Resource):
    """Show a single packet item and lets you delete them"""

    @packet_ns.doc('get_packet')
    @packet_ns.marshal_with(packet)
    def get(self, id):
        """Fetch a given resource"""
        return Packet_DAO.manual_get(id, Type=True)


# Domain
@domain_ns.route('')
class domainList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @domain_ns.doc('list_domain')
    @domain_ns.marshal_list_with(domain)
    def get(self):
        """List all tasks"""
        return Domain_DAO.get()

    @domain_ns.doc('create_domain')
    @domain_ns.expect(domain)
    @domain_ns.marshal_with(domain, code=201)
    def post(self):
        """Create a new task"""
        return Domain_DAO.create(api.payload), 201


@domain_ns.route('/<int:id>')
@domain_ns.response(404, 'domain not found')
@domain_ns.param('id', 'The domain identifier')
class Domain(Resource):
    """Show a single packet item and lets you delete them"""

    @domain_ns.doc('get_domain')
    @domain_ns.marshal_with(domain)
    def get(self, id):
        """Fetch a given resource"""
        return Domain_DAO.get(id, Type=True)


# Job
@job_ns.route('')
class JobList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @job_ns.doc('list_Jobs')
    @job_ns.marshal_list_with(job)
    def get(self):
        """List all tasks"""
        return Job_DAO.get()

    @job_ns.doc('create_Jobs')
    @job_ns.expect(job)
    @job_ns.marshal_with(packet, code=201)
    def post(self):
        """Create a new task"""
        return Job_DAO.create(api.payload), 201


@job_ns.route('/<int:id>')
@job_ns.response(404, 'Jobs not found')
@job_ns.param('id', 'The task identifier')
class Job(Resource):
    """Show a single job item and lets you delete them"""

    @job_ns.doc('get_packet')
    @job_ns.marshal_with(job)
    def get(self, id):
        """Fetch a given resource"""
        return Job_DAO.get(id, Type=True)


# Systeminfo
@systeminfo_ns.route('')
class systeminfotList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @systeminfo_ns.doc('list_systeminfo')
    @systeminfo_ns.marshal_list_with(systeminfo)
    def get(self):
        """List all tasks"""
        return Systeminfo_DAO.get()

    @systeminfo_ns.doc('create_packet')
    @systeminfo_ns.expect(systeminfo)
    @systeminfo_ns.marshal_with(systeminfo, code=201)
    def post(self):
        """Create a new task"""
        return Systeminfo_DAO.create(api.payload), 201


@systeminfo_ns.route('/<int:id>')
@systeminfo_ns.response(404, 'systeminfo not found')
@systeminfo_ns.param('id', 'The task identifier')
class Systeminfo(Resource):
    """Show a single packet item and lets you delete them"""

    @systeminfo_ns.doc('get_packet')
    @systeminfo_ns.marshal_with(systeminfo)
    def get(self, id):
        """Fetch a given resource"""
        return Systeminfo_DAO.get(id, Type=True)


# ports
@ports_ns.route('')
class porttList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @ports_ns.doc('list_ports')
    @ports_ns.marshal_list_with(ports)
    def get(self):
        """List all tasks"""
        return Ports_DAO.get()

    @ports_ns.doc('create_packet')
    @ports_ns.expect(ports)
    @ports_ns.marshal_with(ports, code=201)
    def post(self):
        """Create a new task"""
        return Ports_DAO.create(api.payload), 201


@ports_ns.route('/<int:id>')
@ports_ns.response(404, 'ports not found')
@ports_ns.param('id', 'The task identifier')
class Ports(Resource):
    """Show a single packet item and lets you delete them"""

    @ports_ns.doc('get_ports')
    @ports_ns.marshal_with(ports)
    def get(self, id):
        """Fetch a given resource"""
        return Ports_DAO.get(id, Type=True)


# CSP Evaluator
@csp_evaluator_ns.route('')
class csp_evaluatorList(Resource):
    """Shows a list of all csp_evaluator, and lets you POST to add new tasks"""

    @csp_evaluator_ns.doc('list_csp_evaluator')
    @csp_evaluator_ns.marshal_list_with(csp_evaluator)
    def get(self):
        """List all tasks"""
        return CSPEvaluator_DAO.get()

    @csp_evaluator_ns.doc('create_csp_evaluator')
    @csp_evaluator_ns.expect(csp_evaluator)
    @csp_evaluator_ns.marshal_with(csp_evaluator, code=201)
    def post(self):
        """Create a new task"""
        return CSPEvaluator_DAO.create(api.payload), 201


@csp_evaluator_ns.route('/<int:id>')
@csp_evaluator_ns.response(404, 'csp_evaluator not found')
@csp_evaluator_ns.param('id', 'The task identifier')
class CSPEvaluator(Resource):
    """Show a single csp_evaluator item and lets you delete them"""

    @csp_evaluator_ns.doc('get_csp_evaluator')
    @csp_evaluator_ns.marshal_with(systeminfo)
    def get(self, id):
        """Fetch a given resource"""
        return CSPEvaluator_DAO.get(id, Type=True)


# AttackVector
@attackVector_ns.route('')
class attackVectorList(Resource):
    """Shows a list of all packets, and lets you POST to add new tasks"""

    @attackVector_ns.doc('list_attackVector')
    @attackVector_ns.marshal_list_with(AttackVector)
    def get(self):
        """List all tasks"""
        return AttackVector_DAO.get()

    @attackVector_ns.doc('create_attackVector')
    @attackVector_ns.expect(AttackVector)
    @attackVector_ns.marshal_with(AttackVector, code=201)
    def post(self):
        """Create a new task"""
        return AttackVector_DAO.create(api.payload), 201


@attackVector_ns.route('/<int:id>')
@attackVector_ns.response(404, 'attackVector not found')
@attackVector_ns.param('id', 'The task identifier')
class attackVector(Resource):
    """Show a single packet item and lets you delete them"""

    @attackVector_ns.doc('get_attackVector')
    @attackVector_ns.marshal_with(AttackVector)
    def get(self, id):
        """Fetch a given resource"""
        return AttackVector_DAO.get(id, Type=True)


@attackVector_ns.route('/<string:start>-<string:counting>')
@attackVector_ns.response(404, 'attackVector not found')
@attackVector_ns.param('start', 'The task start')
@attackVector_ns.param('counting', 'The task counting')
class attackVectorData(Resource):
    """Show a attackVector Count data"""

    @attackVector_ns.doc('get attackVector counting data')
    @attackVector_ns.marshal_with(AttackVector)
    def get(self, start, counting):
        """Fetch a given resource"""
        return AttackVector_DAO.retCountbyData(start, counting)


@attackVector_ns.route('/count')
class automation_packetList(Resource):
    """Shows a count of all attackVector data list"""

    @attackVector_ns.doc('count of attackVector list')
    @attackVector_ns.marshal_list_with(AttackVector_Count)
    def get(self):
        """Count of list attackVector data"""
        return {"counting": AttackVector_DAO.count()}


# CVE
@cveInfo_ns.route('/<string:framework>/<string:version>')
class attackVectorList(Resource):
    """Shows a list of all cve"""

    @cveInfo_ns.doc('list_cveInfo')
    @cveInfo_ns.marshal_list_with(cveinfo)
    def get(self, framework, version):
        """List all tasks"""
        return CVEInfo_DAO.Search_get(framework, version)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=20102, debug=True)
