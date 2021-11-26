from flask_sqlalchemy import SQLAlchemy

cve_db = SQLAlchemy()


class job(db.Model):
    __tablename__ = 'job'
    __bind_key__ = 'JOB'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    targetURL = db.Column(db.TEXT, nullable=False)
    knownInfo = db.Column(db.JSON, nullable=False)
    recursiveLevel = db.Column(db.TEXT, nullable=False)
    uriPath = db.Column(db.JSON, nullable=False)  # TEXT
    done = db.Column(db.BOOLEAN, default=False)
    maximumProcess = db.Column(db.TEXT, nullable=0)

    def __init__(self, targetURL, knownInfo, recursiveLevel, uriPath, done, maximumProcess, **kwargs):
        self.targetURL = targetURL
        self.knownInfo = knownInfo
        self.recursiveLevel = recursiveLevel
        self.uriPath = uriPath
        self.done = done
        self.maximumProcess = maximumProcess

    def __repr__(self):
        return f"<job('{self.targetURL}', '{self.knownInfo}', '{self.recursiveLevel}', '{self.uriPath}', '{self.done}', '{self.maximumProcess}')>"
