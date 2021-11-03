from API import BWASP_DB


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
