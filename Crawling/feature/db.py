import sqlalchemy as db
import os
import json
import datetime
from urllib.parse import urlparse,urlunparse
from bs4 import BeautifulSoup

from sqlalchemy.orm import relation

def get_dbpath(repo_name="BWASP",prefix="sqlite:///",sub_path="Web\databases\BWASP.db"):
    repopath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    index = repopath.find(repo_name)
    repopath = repopath[:index+len(repo_name)]
    return (prefix+repopath+"\\"+sub_path).replace("\\","\\\\")

def isSameDomain(target_url, visit_url):
    try:
        target = urlparse(target_url)
        visit = urlparse(visit_url)

        if visit.scheme != "http" and visit.scheme != "https":
            return False
        if target.netloc == visit.netloc:
            return True
        else:
            return False
    except:
        return False

def connect(table_name):
    db_path =get_dbpath()
    db_engine = db.create_engine(db_path)
    db_connect = db_engine.connect()
    db_metadata = db.MetaData()
    db_table = db.Table(table_name, db_metadata, autoload=True, autoload_with=db_engine)
    
    return db_connect, db_table

def insertPackets(req_res_packets):
    db_connect, db_table = connect("packets")

    for packet in req_res_packets:
        status_code = packet["response"]["status_code"]
        request_type = packet["request"]["method"]
        request_json = json.dumps(packet["request"])
        resonse_header = json.dumps(packet["response"]["headers"])
        response_body = packet["response"]["body"]


        #form tag action and input tag and input name parse
        soup = BeautifulSoup(response_body, 'html.parser')
        text = soup.find_all('input')
        try:
            form = soup.find_all('form')
        except:
            form = "none"
        print("TEST TOP9")

        for tag in text:
            if tag.attrs['type'] != "submit" and len(text) != 0:
                print(tag) #input tag 값 ex) <input ~
                print(tag.attrs['name']) #parameter name 값 ex) uname

        if form != "none":
            for tag in form:
                print(tag.attrs['action'])


        query = db.insert(db_table).values(statusCode=status_code, requestType=request_type, requestJson=request_json,
                                            responseHeader=resonse_header, responseBody=response_body)
        result = db_connect.execute(query)
        result.close()


def insertCSP(csp_result):
    db_connect, db_table = connect("CSPEvaluator")
    UUID = 0

    query = db.select([db_table]).where(db_table.columns.UUID == UUID)
    row = db_connect.execute(query).fetchall()

    if len(row) != 0:
        query = db.update(db_table).where(db_table.columns.UUID == UUID).values(header = json.dumps(csp_result))
        result = db_connect.execute(query)
        result.close()
    else:
        query = db.insert(db_table).values(UUID=0, header=json.dumps(csp_result), analysis='None', status='None')
        result = db_connect.execute(query)
        result.close()

# TODO
# 중복된 url 이 있을 경우, 데이터를 넣어야 하는가?
def insertDomains(req_res_packets, cookie_result, previous_packet_count, target_url):
    db_connect, db_table = connect("domain")
    '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    relatePacket = db.Column(db.Integer, nullable=False)
    URL = db.Column(db.TEXT(1000), nullable=False)
    URI = db.Column(db.TEXT(1000), nullable=False)
    params = db.Column(db.TEXT(1000), nullable=False)
    cookie = db.Column(db.TEXT(1000), nullable=False)
    authType = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.TEXT(1000), nullable=False)
    '''

    '''
    id: primary key
    relatedPacket: packet 
    url: http://kitribob.kr/
    uri: /asdf/1.php
    param: 인자 값 (json)
    cookie: cookie value (json)
    authType: 인증이 없는 페이지 0, 로그인 같은 일반 인증 1, 토큰 2
    comment: 해당 페이지의 주석
    '''

    for i,packet in enumerate(req_res_packets):
        if not isSameDomain(target_url, packet["request"]["full_url"]):
            continue

        url_part=urlparse(packet["request"]["full_url"])
        domain_url=urlunparse(url_part._replace(params="",query="",fragment="", path=""))
        domain_uri=urlunparse(url_part._replace(scheme="",netloc=""))
        domain_params = packet["request"]["body"] if packet["request"]["body"] else "None"

        if not packet["request"]["full_url"] in cookie_result.keys():
            domain_cookie = 'None'
        else:
            domain_cookie = json.dumps(cookie_result[packet["request"]["full_url"]])
        #패킷 url이 중복된다면 ??
        #json.dumps()
        #getPacketIndex
        # TODO
        # GET 데이터를 params 에 넣어야 할까?
        query = db.insert(db_table).values(relatePacket=previous_packet_count+i+1, URL=domain_url,
                                            URI=domain_uri, params=domain_params,cookie=domain_cookie,authType=0,comment='None')
        result = db_connect.execute(query)
        result.close()

def insertPorts(port_list, target_url):
    db_connect, db_table = connect("ports")

    for service in port_list.keys():
        query = db.insert(db_table).values(service=service, target=target_url, 
                                            port=port_list[service], result="Open")
        result = db_connect.execute(query)
        result.close()
    else:
        query = db.insert(db_table).values(service="None", target=target_url, 
                                            port="None", result="None")
        result = db_connect.execute(query)
        result.close()

def insertWebInfo(analyst_result, target_url, previous_packet_count):
    db_connect, db_table = connect("systeminfo")

    query = db.select([db_table]).where(db_table.columns.url == target_url)
    row = db_connect.execute(query).fetchall()
    
    for category in analyst_result:
        for key in analyst_result[category]:
            analyst_result[category][key]["request"] = analyst_result[category][key]["request"][:1]
            analyst_result[category][key]["response"] = analyst_result[category][key]["response"][:1]

            if len(analyst_result[category][key]["request"]) != 0:
                analyst_result[category][key]["request"][0] = getPacketIndex(analyst_result[category][key]["request"][0], previous_packet_count)
            if len(analyst_result[category][key]["response"]) != 0:
                analyst_result[category][key]["response"][0] = getPacketIndex(analyst_result[category][key]["response"][0], previous_packet_count)

    if len(row) == 0:
        query = db.insert(db_table).values(url=target_url, data=json.dumps(analyst_result))
        result = db_connect.execute(query)
        result.close()
    else:
        query = db.update(db_table).where(db_table.columns.url == target_url).values(data = json.dumps(analyst_result))
        result = db_connect.execute(query)
        result.close()

# 한번 방문할 때마다 실행되기 때문에 느릴거 같음.
def getPacketsCount():
    db_connect, db_table = connect("packets")

    query = db.select([db_table])
    row = db_connect.execute(query).fetchall()
    
    return len(row)

def getPacketIndex(packet_index, previous_packet_count):
    return previous_packet_count + packet_index + 1