from API import BWASP_DB


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
