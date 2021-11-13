from flask_sqlalchemy import SQLAlchemy

bwasp_db = SQLAlchemy()


class packets(bwasp_db.Model):
    __tablename__ = 'packets'
    __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    category = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    statusCode = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    requestType = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    requestJson = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    responseHeader = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    responseBody = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

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


class domain(bwasp_db.Model):
    __tablename__ = 'domain'
    __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    related_Packet = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    URL = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    URI = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    action_URL = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    action_URL_Type = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    params = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    comment = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    attackVector = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    impactRate = bwasp_db.Column(bwasp_db.Integer, nullable=False)
    description = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    Details = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

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


class job(bwasp_db.Model):
    __tablename__ = 'job'
    __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    targetURL = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    knownInfo = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    recursiveLevel = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    uriPath = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}')>"


class ports(bwasp_db.Model):
    __tablename__ = 'ports'
    __bind_key__ = 'BWASP'
    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    service = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    target = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    port = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    result = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

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
    url = bwasp_db.Column(bwasp_db.TEXT, nullable=False)
    data = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

    def __init__(self, url, data, **kwargs):
        self.url = url
        self.data = data

    def __repr__(self):
        return f"<systeminfo('{self.url}', '{self.data}')>"


class CSPEvaluator(bwasp_db.Model):
    __tablename__ = 'CSPEvaluator'
    __bind_key__ = 'BWASP'

    id = bwasp_db.Column(bwasp_db.Integer, primary_key=True, autoincrement=True)
    header = bwasp_db.Column(bwasp_db.TEXT, nullable=False)

    def __init__(self, header, **kwargs):
        self.header = header

    def __repr__(self):
        return f"<CSPEvaluator('{self.UUID}', '{self.header}')>"
