# from Web.app import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class attackVector(db.Model):
    __tablename__ = 'attackVector'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attackVector = db.Column(db.TEXT(1000), nullable=False)
    typicalServerity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.TEXT(1000), nullable=False)
    vlunClass = db.Column(db.TEXT(1000), nullable=False)


class CSPEmulator(db.Model):
    __tablename__ = 'CSPEmulator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UUID = db.Column(db.Integer, nullable=False)
    header = db.Column(db.TEXT(1000), nullable=False)
    analysis = db.Column(db.TEXT(1000), nullable=False)
    status = db.Column(db.TEXT(1000), nullable=False)
    createTime = db.Column(db.DateTime, nullable=False)


class domain(db.Model):
    __tablename__ = 'domain'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    relatePacket = db.Column(db.Integer, nullable=False)
    URL = db.Column(db.TEXT(1000), nullable=False)
    URI = db.Column(db.TEXT(1000), nullable=False)
    params = db.Column(db.TEXT(1000), nullable=False)
    cookie = db.Column(db.TEXT(1000), nullable=False)
    authType = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.TEXT(1000), nullable=False)


class job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    targetURL = db.Column(db.TEXT(1000), nullable=False)
    knownInfo = db.Column(db.TEXT(1000), nullable=False)
    recursiveLevel = db.Column(db.TEXT(1000), nullable=False)
    uriPath = db.Column(db.TEXT(1000), nullable=False)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, **kargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}, {self.uriPath}')>"


class packets(db.Model):
    __tablename__ = 'packets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statusCode = db.Column(db.Integer, nullable=False)
    requestType = db.Column(db.TEXT(1000), nullable=False)
    requestJson = db.Column(db.TEXT(1000), nullable=False)
    responseHeader = db.Column(db.TEXT(1000), nullable=False)
    responseBody = db.Column(db.TEXT(1000), nullable=False)


class ports(db.Model):
    __tablename__ = 'ports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service = db.Column(db.TEXT(1000), nullable=False)
    target = db.Column(db.TEXT(1000), nullable=False)
    port = db.Column(db.TEXT(1000), nullable=False)
    result = db.Column(db.TEXT(1000), nullable=False)


class systeminfo(db.Model):
    __tablename__ = 'systeminfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    relatedPacket = db.Column(db.Integer, nullable=False)
    reliability = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    data = db.Column(db.TEXT(1000), nullable=False)
    language = db.Column(db.TEXT(1000), nullable=False)
    method = db.Column(db.TEXT(1000), nullable=False)


class URIAnalysis(db.Model):
    __tablename__ = 'URIAnalysis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UUID = db.Column(db.Integer, nullable=False)
    URI = db.Column(db.TEXT(1000), nullable=False)
    analysis = db.Column(db.TEXT(1000), nullable=False)
    description = db.Column(db.TEXT(1000), nullable=False)
    insertPoints = db.Column(db.Integer, nullable=False)


class Charts(db.Model):
    __tablename__ = 'Charts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.TEXT(1000), nullable=False)
    data = db.Column(db.TEXT(1000), nullable=False)
    ratio = db.Column(db.Integer, nullable=False)
    insertPoints = db.Column(db.Integer, nullable=False)
