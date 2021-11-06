from API import BWASP_DB


class CSPEvaluator(BWASP_DB.Model):
    __tablename__ = 'CSPEvaluator'
    __bind_key__ = 'BWASP'

    id = BWASP_DB.Column(BWASP_DB.Integer, primary_key=True, autoincrement=True)
    header = BWASP_DB.Column(BWASP_DB.TEXT, nullable=False)

    def __init__(self, header, **kwargs):
        self.header = header

    def __repr__(self):
        return f"<CSPEvaluator('{self.UUID}', '{self.header}')>"
