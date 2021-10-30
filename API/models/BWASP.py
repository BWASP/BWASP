# from Web.app import bwasp_db
from flask_sqlalchemy import SQLAlchemy

bwasp_db = SQLAlchemy()


class CSPEvaluator(bwasp_db.Model):
    __tablename__ = 'CSPEvaluator'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    UUID = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    header = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    analysis = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    status = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, UUID, header, analysis, status, **kwargs):
        self.UUID = UUID
        self.header = header
        self.analysis = analysis
        self.status = status

    def __repr__(self):
        return f"<CSPEvaluator('{self.UUID}', '{self.header}', '{self.analysis}', '{self.status}')>"


class domain(bwasp_db.Model):
    __tablename__ = 'domain'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    relatePacket = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    URL = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    URI = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    params = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    cookie = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    # authType = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    comment = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, relatePacket, URL, URI, params, cookie, authType, comment, **kwargs):
        self.relatePacket = relatePacket
        self.URL = URL
        self.URI = URI
        self.params = params
        self.cookie = cookie
        # self.authType = authType
        self.comment = comment

    def __repr__(self):
        # return f"<domain('{self.relatePacket}', '{self.URL}', '{self.params}', '{self.cookie}', '{self.authType}', '{self.comment}')>"
        return f"<domain('{self.relatePacket}', '{self.URL}', '{self.params}', '{self.cookie}', '{self.comment}')>"


class job(bwasp_db.Model):
    __tablename__ = 'job'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    targetURL = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    knownInfo = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    recursiveLevel = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    uriPath = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}')>"


class packets(bwasp_db.Model):
    __tablename__ = 'packets'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    category = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    statusCode = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    requestType = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    requestJson = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    responseHeader = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    responseBody = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, category, statusCode, requestType, requestJson, responseHeader, responseBody, **kwargs):
        self.category = category
        self.statusCode = statusCode
        self.requestType = requestType
        self.requestJson = requestJson
        self.responseHeader = responseHeader
        self.responseBody = responseBody

    def __repr__(self):
        return f"<packets('{self.category}', '{self.statusCode}', '{self.requestType}', '{self.requestJson}', '{self.responseHeader}', '{self.responseBody}')>"


class ports(bwasp_db.Model):
    __tablename__ = 'ports'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    service = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    target = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    port = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    result = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, service, target, port, result, **kwargs):
        self.service = service
        self.target = target
        self.port = port
        self.result = result

    def __repr__(self):
        return f"<ports('{self.service}', '{self.target}', '{self.port}, {self.result}')>"


class systeminfo(bwasp_db.Model):
    __tablename__ = 'systeminfo'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    url = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    data = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, url, data, **kwargs):
        self.url = url
        self.data = data

    def __repr__(self):
        return f"<systeminfo('{self.url}', '{self.data}')>"


"""
class URIAnalysis(bwasp_db.Model):
    __tablename__ = 'URIAnalysis'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    UUID = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    URI = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    analysis = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    description = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    insertPoints = bwasp_db.Column(bwasp_db.Integer, nullable=False)

    def __init__(self, UUID, URI, analysis, description, insertPoints, **kwargs):
        self.UUID = UUID
        self.URI = URI
        self.analysis = analysis
        self.description = description
        self.insertPoints = insertPoints

    def __repr__(self):
        return f"<URIAnalysis('{self.UUID}', '{self.URI}', '{self.analysis}', '{self.description}', '{self.insertPoints}')>"
"""


class attackVector(bwasp_db.Model):
    __tablename__ = 'attackVector'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    UUID = bwasp_db.Column(bwasp_db.Integer, nullable=True)
    attackVector = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    typicalServerity = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    description = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    # vulnClass = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)

    def __init__(self, UUID, attackVector, typicalServerity, description, **kwargs):
        self.UUID = UUID
        self.attackVector = attackVector
        self.typicalServerity = typicalServerity
        self.description = description

    def __repr__(self):
        return f"<attackVector('{self.UUID}', '{self.attackVector}', '{self.typicalServerity}', '{self.description}')>"


"""
class Charts(bwasp_db.Model):
    __tablename__ = 'Charts'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    type = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    name = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    data = bwasp_db.Column(bwasp_db.TEXT(1000), nullable=False)
    ratio = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    insertPoints = bwasp_db.Column(bwasp_db.Integer, nullable=False)

    def __init__(self, type, name, data, ratio, insertPoints, **kwargs):
        self.type = type
        self.name = name
        self.data = data
        self.ratio = ratio
        self.insertPoints = insertPoints

    def __repr__(self):
        return f"<Charts('{self.type}', '{self.name}', '{self.data}', '{self.ratio}', '{self.insertPoints}')>"
"""
