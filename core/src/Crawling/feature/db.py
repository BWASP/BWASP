import os, json, requests
from urllib.parse import urlparse, urlunparse

from .func import *
from Crawling.attack_vector import *
from .api import (
    Packets as APIofPackets,
    Domain as APIofDomain,
    CSPEvaluator as APIofCSPEvaluator,
    Job as APIofJob,
    SystemInfo as APIofSystemInfo,
    Ports as APIofPorts
)


class Packets:
    def __init__(self):
        self.reqData = list()
        self.packetsFormat = {
            "statusCode": 0,
            "requestType": "",
            "requestJson": "",
            "responseHeader": "",
            "responseBody": ""
        }

    def insertPackets(self, req_res_packets):
        for packetData in req_res_packets:
            self.packetsFormat["statusCode"] = packetData["response"]["status_code"]
            self.packetsFormat["requestType"] = packetData["request"]["method"]
            self.packetsFormat["requestJson"] = packetData["request"]
            self.packetsFormat["responseHeader"] = packetData["response"]["headers"]
            self.packetsFormat["responseBody"] = packetData["response"]["body"]

        self.reqData.append(self.packetsFormat)

        APIofPackets().PostAutomation(json.dumps(self.reqData))

    @staticmethod
    def getPacketIndex(packet_index, previous_packet_count):
        return previous_packet_count + packet_index + 1


class CSPEvaluator:
    def __init__(self):
        self.reqData = list()
        self.CSPEvaluatorFormat = {
            "header": ""
        }

    def insertCSP(self, csp_result):
        self.CSPEvaluatorFormat["header"] = csp_result
        self.reqData.append(self.CSPEvaluatorFormat)

        APIofCSPEvaluator().PostCSPEvaluator(json.dumps(self.reqData))


class Domains:
    def __init__(self):
        pass

    # TODO: 중복된 url 이 있을 경우, 데이터를 넣어야 하는가?
    def insertDomains(self, req_res_packets, cookie_result, packet_indexes, target_url, analysis_data):
        """
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
        """

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
            if not isSameDomain(target_url, packet["request"]["full_url"]):
                continue
            if isExistExtension(packet["request"]["full_url"], ["image", "style", "font"]):
                continue
            # 공격 벡터 input 태그 분석 input_tag 함수는 attack_vector.py에서 사용하는 함수
            response_body = packet["response"]["body"]
            tag_list, tag_name_list, attack_vector, action_page, action_type, impactRate = inputTag(response_body, analysis_data["http_method"], analysis_data["infor_vector"])

            cors_check = corsCheck(packet)
            if cors_check != "None":
                attack_vector["doubt"]["CORS"] = True
                impactRate = 2
            else:
                attack_vector["doubt"].pop("CORS")

            url_part = urlparse(packet["request"]["full_url"])
            domain_url = urlunparse(url_part._replace(params="", query="", fragment="", path=""))
            domain_uri = urlunparse(url_part._replace(scheme="", netloc=""))

            # if len(domain_params) > 0:

            tag_name_list.append(url_part.query)  # hello=world&a=b
            # domain_params = packet["request"]["body"] if packet["request"]["body"] else "None"

            # Query String 정리
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

            # robots.txt check
            if analysis_data["robots_result"] == True:
                attack_vector["misc"]["robots.txt"] = analysis_data["robots_result"]
            else:
                attack_vector["misc"].pop("robots.txt")

            # Error Page check
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
            # TODO: GET 데이터를 params 에 넣어야 할까?
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

        APIofDomain().PostDomain(json.dumps(data))


class Ports:
    def __init__(self):
        self.reqData = list()
        self.portsFormat = {
            "service": "",
            "target": "",
            "port": "",
            "result": "Open"  # prefixed
        }

    def insertPorts(self, port_list, target_url):
        for services in port_list.keys():
            self.portsFormat["service"] = port_list[services]
            self.portsFormat["target"] = target_url
            self.portsFormat["port"] = services

        self.reqData.append(self.portsFormat)

        APIofPorts().PostPorts(json.dumps(self.reqData))


class SystemInformation:
    def __init__(self):
        self.reqData = list()
        self.portsFormat = {
            "POST": {
                "url": input_url,
                "data": "None"  # prefixed
            },
            "UPDATE": {
                "id": 1,  # prefixed
                "data": analyst_result
            }
        }

    def postWebInfo(self, input_url):
        self.portsFormat["POST"]["url"] = input_url
        self.reqData.append(self.portsFormat["POST"])

        SystemInfo().PostSystemInfo(json.dumps(self.reqData))

    def updateWebInfo(self, analyst_result):
        self.portsFormat["UPDATE"]["data"] = analyst_result
        self.reqData.append(self.portsFormat["UPDATE"])

        APIofSystemInfo().PATCHSystemInfo(json.dumps(self.reqData))
