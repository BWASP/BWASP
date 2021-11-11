# from Web.app import BWASP_DB
from flask_sqlalchemy import SQLAlchemy

BWASP_DB = SQLAlchemy()


class packets(BWASP_DB.Model):
    __tablename__ = 'packets'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    category = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    statusCode = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    requestType = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    requestJson = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    responseHeader = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    responseBody = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, category, statusCode, requestType, requestJson, responseHeader, responseBody, **kwargs):
        self.category = category
        self.statusCode = statusCode
        self.requestType = requestType
        self.requestJson = requestJson
        self.responseHeader = responseHeader
        self.responseBody = responseBody

    def __repr__(self):
        return f"<packets('{self.category}', '{self.statusCode}', '{self.requestType}', '{self.requestJson}', " \
               f"'{self.responseHeader}', '{self.responseBody}')>"


class domain(BWASP_DB.Model):
    __tablename__ = 'domain'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    related_Packet = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    URL = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    URI = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    action_URL = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    action_URL_Type = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    params = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    comment = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    attackVector = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    impactRate = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    description = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    Details = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, related_Packet, URL, URI, action_URL, action_URL_Type, params, comment, attackVector, impactRate, description, Details, **kwargs):
        self.related_Packet = related_Packet
        self.URL = URL
        self.URI = URI
        self.action_URL = action_URL
        self.action_URL_Type = action_URL_Type
        self.params = params
        self.comment = comment
        self.attackVector = attackVector
        self.impactRate = impactRate
        self.description = description
        self.Details = Details

    def __repr__(self):
        return f"<domain('{self.related_Packet}', '{self.URL}', '{self.URI}', '{self.action_URL}', '{self.action_URL_Type}', '{self.params}', '{self.comment}', " \
               f"'{self.attackVector}', '{self.impactRate}', '{self.description}', '{self.Details}')>"


class job(BWASP_DB.Model):
    __tablename__ = 'job'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    targetURL = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    knownInfo = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    recursiveLevel = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    uriPath = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}')>"


class ports(BWASP_DB.Model):
    __tablename__ = 'ports'
    __bind_key__ = 'BWASP'
    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    service = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    target = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    port = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    result = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, service, target, port, result, **kwargs):
        self.service = service
        self.target = target
        self.port = port
        self.result = result

    def __repr__(self):
        return f"<ports('{self.service}', '{self.target}', '{self.port}, {self.result}')>"


class systeminfo(BWASP_DB.Model):
    __tablename__ = 'systeminfo'
    __bind_key__ = 'BWASP'
    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    url = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    data = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, url, data, **kwargs):
        self.url = url
        self.data = data

    def __repr__(self):
        return f"<systeminfo('{self.url}', '{self.data}')>"


class CSPEvaluator(BWASP_DB.Model):
    __tablename__ = 'CSPEvaluator'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    header = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, header, **kwargs):
        self.header = header

    def __repr__(self):
        return f"<CSPEvaluator('{self.UUID}', '{self.header}')>"
