from API.app import BWASP_DB


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
