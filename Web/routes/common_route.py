from flask import (
    Blueprint, render_template, g
)
from Web.models.BWASP import attackVector, CSPEmulator, domain, packets
import json

from Web.models.BWASP import db, domain, systeminfo, attackVector

import sqlalchemy as db2
from sqlalchemy import and_, desc
import os

NAME = 'common'
bp = Blueprint(NAME, __name__, url_prefix='/common')

#절대경로
def get_dbpath(repo_name="BWASP",prefix="sqlite:///",sub_path="Web\databases\CVE.db"):
    repopath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    index = repopath.find(repo_name)
    repopath = repopath[:index+len(repo_name)]
    return (prefix+repopath+"\\"+sub_path).replace("\\","\\\\")

def cve_Data(search):
    tmp = search.split(' ')
    search_title = tmp[0]
    search_version = tmp[1]
    db_engine = db2.create_engine(get_dbpath())
    db_connection = db_engine.connect()
    db_metadata = db2.MetaData()
    db_table = db2.Table('CVE', db_metadata, autoload=True, autoload_with=db_engine)

    #query = db2.select(db_table).where(db_table.description==search)
    #query = db2.select(db_table).where(db_table.columns.description.like("%"+search+"%"))

    #db2.select(db_table) 만 하면 table 전체 columns.year로 하면 year 컬럼만 해당
    query = db2.select(db_table.columns.year).where(and_(
        db_table.columns.description.like("%"+search_title+"%"), db_table.columns.description.like("%"+search_version+"%"))).order_by(
        db_table.columns.year.desc())

    result = db_connection.execute(query)
    result_set = result.fetchall()
    cve_data = str(result_set[0]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    return cve_data


@bp.route('/export')
def bpExport():
    return render_template('common/export.html', Title="Export report - BWASP")


@bp.route('/attack_vector')
def attack_Vector():
    g.db = db.session()
    domain_data = g.db.query(domain).all()
    systeminfo_data = g.db.query(systeminfo).all()
    attackVector_data = g.db.query(attackVector).all()
    print("URL: "+domain_data[0].URL+domain_data[0].URI)
    print("Vulnerability Doubt: " + attackVector_data[0].attackVector)
    cve_data = cve_Data(systeminfo_data[2].data)
    return render_template('common/AttackVector.html', Title="Attack Vectors - BWASP", data="result",
                           domain_data=domain_data[0].URL+domain_data[0].URI,
                           attackVector_data=attackVector_data[0].attackVector,
                           systeminfo_data=systeminfo_data[2].data, cve_data=cve_data)
