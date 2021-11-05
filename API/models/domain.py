from API import BWASP_DB


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
    typicalServerity = BWASP_DB.Column(BWASP_DB.Integer, nullable=False)
    description = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)
    Details = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, related_Packet, URL, URI, action_URL, action_URL_Type, params, comment, attackVector, typicalServerity, description, Details, **kwargs):
        self.related_Packet = related_Packet
        self.URL = URL
        self.URI = URI
        self.action_URL = action_URL
        self.action_URL_Type = action_URL_Type
        self.params = params
        self.comment = comment
        self.attackVector = attackVector
        self.typicalServerity = typicalServerity
        self.description = description
        self.Details = Details

    def __repr__(self):
        return f"<domain('{self.related_Packet}', '{self.URL}', '{self.URI}', '{self.action_URL}', '{self.action_URL_Type}', '{self.params}', '{self.comment}', " \
               f"'{self.attackVector}', '{self.typicalServerity}', '{self.description}', '{self.Details}')>"

