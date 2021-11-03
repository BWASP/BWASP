from API import BWASP_DB


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
