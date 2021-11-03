from API import BWASP_DB


class domain(BWASP_DB.Model):
    __tablename__ = 'domain'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    related_Packet = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    URL = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    URI = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    params = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    comment = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    attackVector = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    typicalServerity = BWASP_DB.Column(BWASP_DB.INT, nullable=False)
    description = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    Details = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, relatePacket, URL, URI, params, comment, attackVector, typicalServer, description, Details, **kwargs):
        self.relatePacket = relatePacket
        self.URL = URL
        self.URI = URI
        self.params = params
        self.comment = comment
        self.attackVector = attackVector
        self.typicalServerity = typicalServer
        self.description = description
        self.Details = Details

    def __repr__(self):
        return f"<domain('{self.relatePacket}', '{self.URL}', '{self.URI}', '{self.params}', '{self.comment}', '{self.attackVector}', '{self.typicalServerity}', '{self.description}', '{self.Details}')>"
