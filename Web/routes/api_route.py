from flask import (
    Blueprint, render_template,
    g, jsonify
)
from Web.models.BWASP import db, domain, systeminfo, attackVector, packets
import sqlalchemy as db2
from sqlalchemy import and_, desc
import os, json, datetime

NAME = 'api'
bp = Blueprint(NAME, __name__, url_prefix='/api')


# 절대경로
def get_dbpath(repo_name="BWASP", prefix="sqlite:///", sub_path="Web\databases\CVE.db"):
    repopath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    index = repopath.find(repo_name)
    repopath = repopath[:index + len(repo_name)]
    return (prefix + repopath + "\\" + sub_path).replace("\\", "\\\\")


def cve_Data(search):
    server_title_all = search['webserver']
    server_title = list(server_title_all)[0]
    server_version = server_title_all[server_title]['version']
    backend_title_all = search['backend']
    backend_title = ""
    backend_version = ""
    if len(list(backend_title_all)) > 1:
        for i in range(len(list(backend_title_all))):
            backend_title = list(backend_title_all)
            backend_version += backend_title_all[backend_title[i]]['version']
    else:
        backend_title = list(backend_title_all)[0]
        backend_version = backend_title_all[backend_title[0]]['version']

    db_engine = db2.create_engine(get_dbpath())
    db_connection = db_engine.connect()
    db_metadata = db2.MetaData()
    db_table = db2.Table('CVE', db_metadata, autoload=True, autoload_with=db_engine)

    # query = db2.select(db_table).where(db_table.description==search)
    # query = db2.select(db_table).where(db_table.columns.description.like("%"+search+"%"))

    # db2.select(db_table) 만 하면 table 전체 columns.year로 하면 year 컬럼만 해당
    query = db2.select(db_table.columns.year).where(and_(
        db_table.columns.description.like("%" + server_title + "%"), db_table.columns.description.like("%" + server_version + "%"))).order_by(
        db_table.columns.year.desc())

    for i in range(len(list(backend_title_all))):
        backend_query = db2.select(db_table.columns.year).where(and_(
            db_table.columns.description.like("%" + backend_title[i] + "%"), db_table.columns.description.like("%" + backend_version[i] + "%"))).order_by(
            db_table.columns.year.desc())

    result = db_connection.execute(query)
    result_set = result.fetchall()

    backend_result = db_connection.execute(backend_query)
    backend_result_set = backend_result.fetchall()

    cve_data = str(result_set[0]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    cve_data += str(backend_result_set[0]).replace("(", "").replace(")", "").replace(",", "").replace("'", "")
    return cve_data


@bp.route('/')
def apiInvalidRequest():
    return jsonify({"success": False, "message": "잘못된 요청입니다."})


@bp.route('/job/enroll')
def apiJobEnroll():
    return jsonify({"success": True})


@bp.route('/attack_vector')
def AttackVector():
    g.db = db.session()
    domain_data = g.db.query(domain).all()
    systeminfo_data = g.db.query(systeminfo).all()
    attackVector_data = g.db.query(attackVector).all()
    # print("URL: " + domain_data[0].URL + domain_data[0].URI)
    # print("Vulnerability Doubt: " + attackVector_data[0].attackVector)
    # cve_data = cve_Data(systeminfo_data[2].data)
    packets_data = g.db.query(packets).all()

    # sample
    resDataJson = []
    for i in range(0, len(domain_data)):
        JsonData = {
            "url": domain_data[i].URL + domain_data[i].URI,  # "https://naver.com" [URL], /asdf/index.php [URI]
            "payloads": [
                domain_data[i].URI
                # "/index.php",
                # "/class.php"
            ],
            "vulnerability": {
                "type": "1",#attackVector_data[i].attackVector,
                # "Cross Site Script(XSS)",  # (stored, reflected, dom) 으로 XSS 분리하면 될 듯...?
                "CVE": [
                    {
                        "numbering": cve_Data(eval(systeminfo_data[0].data))  # "2021-0000-1111"
                    }
                ]
            },
            "method": packets_data[i].requestType,
            "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # "2021-09-28 11:00",
            "impactRate": 0
        }
        resDataJson.append(JsonData)

        """
        try:
            JsonData = {
                "url": domain_data[i].URL + domain_data[i].URI,  # "https://naver.com" [URL], /asdf/index.php [URI]
                "payloads": [
                    domain_data[i].URI
                    # "/index.php",
                    # "/class.php"
                ],
                "vulnerability": {
                    "type": attackVector_data[i].attackVector,  # "Cross Site Script(XSS)",  # (stored, reflected, dom) 으로 XSS 분리하면 될 듯...?
                    "CVE": [
                        {
                            "numbering": cve_Data(systeminfo_data[0].data)  # "2021-0000-1111"
                        }
                    ]
                },
                "method": "None",
                "date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # "2021-09-28 11:00",
                "impactRate": 0
            }
            resDataJson.append(JsonData)
        except:
            JsonData = {
                "url": "None",
                "payloads": [
                    "None"
                ],
                "vulnerability": {
                    "type": "None",
                    "CVE": [
                        {
                            "numbering": "None"
                        }
                    ]
                },
                "method": "None",
                "date": "None",
                "impactRate": "None"
            }
            resDataJson.append(JsonData)
            break
            """

    #print(resDataJson)

    return jsonify(resDataJson)
