import sqlalchemy as db
import os
import json
from urllib.parse import urlparse, urlunparse
import requests

from Crawling.feature import func
from Crawling.attack_vector import *
import requests
from Crawling.feature.api import *


def connect(table_name):
    db_path = func.get_dbpath()
    db_engine = db.create_engine(db_path)
    db_connect = db_engine.connect()
    db_metadata = db.MetaData()
    db_table = db.Table(table_name, db_metadata, autoloadk=True, autoload_with=db_engine)

    return db_connect, db_table


# REST API: 종민 Packets
def insertPackets(req_res_packets):
    api_url = "http://localhost:20102/api/packets/automation"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = []

    for packet in req_res_packets:
        params = {
            "statusCode": packet["response"]["status_code"],
            "requestType": packet["request"]["method"],
            "requestJson": packet["request"],
            "responseHeader": packet["response"]["headers"],
            "responseBody": packet["response"]["body"]
        }
        data.append(params)

    Packets().PostAutomation(json.dumps(data))
    # res = requests.post(api_url, headers=headers, data=json.dumps(data))


# REST API: 주원 CSP, Ports
def insertCSP(csp_result):
    ### REST API Code
    # url = "http://localhost:20102/api/csp_evaluator"
    data_format = dict()
    csp_data = list()
    data_format["header"] = csp_result
    csp_data.append(data_format)
    csp_data = json.dumps(csp_data)
    CSPEvaluator().PostCSPEvaluator(csp_data)


# REST API: 도훈 Domains
# TODO
# 중복된 url 이 있을 경우, 데이터를 넣어야 하는가?
def insertDomains(req_res_packets, cookie_result, packet_indexes, target_url, analysis_data):
    # db_connect, db_table = connect("domain")
    '''
    [
    {
    "id": 0,
    "relatePacket": 0
    "URL": "string",
    "URI": "string",
    "params": "string",
    "comment": "string",
    "attackVector": "string",
    "typicalServerity": "string",
    "description": "string",
    "Details": "string"
    }
    ]
    '''

    '''
    id: primary key
    relatedPacket: packet 
    url: http://kitribob.kr/
    uri: /asdf/1.php
    param: 인자 값 (json)
    comment: 해당 페이지의 주석
    attackVector: SQL Injection, XSS
    typeicalServerity: 0 (취약점 영향도 low, normal, high)
    description: 취약점 설명 또는 관련 url
    Details: input tag, cookie, query string(get params) json 형태로
    '''

    data = []

    for i, packet in enumerate(req_res_packets):
        if not func.isSameDomain(target_url, packet["request"]["full_url"]):
            continue
        if func.isExistExtension(packet["request"]["full_url"], ["image", "style", "font"]):
            continue
        # 공격 벡터 input 태그 분석 input_tag 함수는 attack_vector.py에서 사용하는 함수
        response_body = packet["response"]["body"]
        tag_list, tag_name_list, attack_vector, action_page, action_type, impactRate = inputTag(response_body, analysis_data["http_method"], analysis_data["infor_vector"], analysis_data["attack_option"], target_url, packet["request"]["full_url"])

        cors_check = corsCheck(packet)
        if cors_check != "None":
            attack_vector["doubt"]["CORS"] = True
            impactRate = 2
        else:
            attack_vector["doubt"].pop("CORS")
            
        url_part = urlparse(packet["request"]["full_url"])
        domain_url = urlunparse(url_part._replace(params="", query="", fragment="", path=""))
        domain_uri = urlunparse(url_part._replace(scheme="", netloc=""))

        #if len(domain_params) > 0:


        tag_name_list.append(url_part.query) # hello=world&a=b
        #domain_params = packet["request"]["body"] if packet["request"]["body"] else "None"

        #Query String 정리
        domain_params = dict()
        if url_part.query != "":
            try:
                if "&" in url_part.query:
                    param_list = url_part.query.split("&")
                    for param in param_list:
                        domain_params[param.split('=')[0]] = param.split('=')[1]
                else:
                    param = url_part.query
                    domain_params[param.split('=')[0]] = param.split('=')[1]
            except:
                domain_params[param.split('=')[0]] = "None"

        if domain_params:
            if "SQL injection" in attack_vector["doubt"]:
                pass
            else:
                if "<th" in response_body:
                    attack_vector["doubt"]["SQL injection"] = {"type": ["board"]}
                    attack_vector["doubt"]["XSS"] = {"type": ["board"]}
                    impactRate = 2
                else:
                    attack_vector["doubt"]["SQL injection"] = {"type": ["None"]}
                    attack_vector["doubt"]["XSS"] = {"type": ["None"]}
                    impactRate = 1
            

        if not packet["request"]["full_url"] in cookie_result.keys():
            domain_cookie = {}
        else:
            domain_cookie = json.dumps(cookie_result[packet["request"]["full_url"]])

        open_redirect = openRedirectionCheck(packet)
        s3_bucket = s3BucketCheck(packet)
        # jwt_token = jwtCheck(packet)
        if len(open_redirect) != 0:
            attack_vector["doubt"]["Open Redirect"] = open_redirect
            impactRate = 2
        else:
            attack_vector["doubt"].pop("Open Redirect", None)

        if len(s3_bucket) != 0:
            attack_vector["doubt"]["s3"] = s3_bucket
            impactRate = 2
        else:
            attack_vector["doubt"].pop("s3", None)

        #robots.txt check
        if analysis_data["robots_result"] == True:
            attack_vector["misc"]["robots.txt"] = analysis_data["robots_result"]
        else:
            attack_vector["misc"].pop("robots.txt")

        #Error Page check
        if analysis_data["error_result"] == True:
            attack_vector["misc"]["error"] = analysis_data["error_result"]
        else:
            attack_vector["misc"].pop("error")
        
        # directory indexing check
        if len(analysis_data["directory_indexing"]) != 0:
            attack_vector["misc"]["indexing"] = analysis_data["directory_indexing"]
        else:
            attack_vector["misc"].pop("indexing")
        
        # admin page check
        if len(analysis_data["admin_page"]) != 0:
            attack_vector["misc"]["admin page"] = analysis_data["admin_page"]
        else:
            attack_vector["misc"].pop("admin page")

        # 패킷 url이 중복된다면 ??
        # json.dumps()
        # getPacketIndex
        # TODO
        # GET 데이터를 params 에 넣어야 할까?
        query = {
            "related_Packet": packet_indexes[i],
            "URL": domain_url,
            "URI": domain_uri,
            "action_URL": action_page,
            "action_URL_Type": action_type,
            "params": tag_name_list,
            "comment": "None",
            "attackVector": attack_vector,
            "impactRate": impactRate,
            "description": "string",
            "Details": {
                "tag": tag_list,
                "cookie": domain_cookie,
                "queryString": domain_params
            }  # tag_list + domain_cookie + #domain_params 양식에 맞춰서 포함해야 함
        }
        data.append(query)

    Domain().PostDomain(json.dumps(data))


# REST API: 주원 CSP, Ports
def insertPorts(port_list, target_url):
    data = []
    for port in port_list.keys():
        value = {
            "service": port_list[port],
            "target": target_url,
            "port": port,
            "result": "Open"
        }
        data.append(value)
        '''
    else:
        value = {
            "service": "None",
            "target": target_url,
            "port": "None",
            "result": "None"
        }
        data.append(value)
        '''
    Ports().PostPorts(json.dumps(data))


# REST API: 주명 WebInfo
# 맨처음에 url , data를 포함한 post 한번 먼저 실행
def postWebInfo(input_url):
    data = []
    value = {
        "url": input_url,
        "data": "None"
    }
    data.append(value)
    SystemInfo().PostSystemInfo(json.dumps(data))


# 이후로 업데이트를 통해 data 값 갱신
def updateWebInfo(analyst_result):
    data = []
    # db_connect, db_table = connect("systeminfo")
    value = {
        "id": 1,
        "data": analyst_result
    }
    data.append(value)
    # api 수정 전
    #SystemInfo().PATCHSystemInfo(json.dumps(value))
    # api 수정후 아래 코드로 바꾸기
    SystemInfo().PATCHSystemInfo(json.dumps(data))


# 한번 방문할 때마다 실행되기 때문에 느릴거 같음.
# def getPacketsCount():
#    db_connect, db_table = connect("packets")

#    query = db.select([db_table])
#    row = db_connect.execute(query).fetchall()

#    return len(row)


def getPacketIndex(packet_index, previous_packet_count):
    return previous_packet_count + packet_index + 1
