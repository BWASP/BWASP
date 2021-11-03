from flask_sqlalchemy import SQLAlchemy

CVE_DB = SQLAlchemy()


class cve(CVE_DB.Model):
    __tablename__ = 'CVE'
    __bind_key__ = 'CVE'
    id = CVE_DB.Column(CVE_DB.Integer, primary_key=True, autoincrement=True)
    year = CVE_DB.Column(CVE_DB.TEXT, nullable=False)
    description = CVE_DB.Column(CVE_DB.TEXT, nullable=False)
