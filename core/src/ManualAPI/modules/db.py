# =========================== 나중에 다시 참고해야 할 것 ===============================
"""
def deleteUselessBody(packets):
    content_types = ["text/css", "application/font-woff2"]

    for index in range(len(packets)):
        if "content-type" in list(packets[index]["response"]["headers"].keys()):
            for type in content_types:
                if packets[index]["response"]["headers"]["content-type"].find(type) != -1:
                    packets[index]["response"]["body"] = ""

    return packets



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


            def getPacketIndex(packet_index, previous_packet_count):
    return previous_packet_count + packet_index + 1
"""

"""from ManualAPI.modules import func, attack_vector
from ManualAPI.modules.api import *"""
import requests, json, sys, os
from urllib.parse import urlparse, urlunparse

#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules import func
from modules.attack_vector import *
from modules.api import *


# REST API: 종민 Packets
def deleteUselessBody(packets):
    content_types = ["text/css", "application/font-woff2"]

    for index in range(len(packets)):
        if "content-type" in list(packets[index]["response"]["headers"].keys()):
            for type in content_types:
                if packets[index]["response"]["headers"]["content-type"].find(type) != -1:
                    packets[index]["response"]["body"] = ""

    return packets


def insertPackets(req_res_packets):
    api_url = "http://localhost:20102/api/packet/manual"
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

    Packets().PostManual(json.dumps(data))
    # res = requests.post(api_url, headers=headers, data=json.dumps(data))


# REST API: 도훈 Domains
# TODO
# 중복된 url 이 있을 경우, 데이터를 넣어야 하는가?
def insertDomains(req_res_packets, cookie_result, packet_indexes, target_url, http_method, infor_vector, robots_result, error_result):
    data = list()
    crx = list()
    for i, packet in enumerate(req_res_packets):
        if not func.isSameDomain(target_url, packet["request"]["full_url"]):
            continue
        if func.isExistExtension(packet["request"]["full_url"], ["image", "style", "font"]):
            continue
        # 공격 벡터 input 태그 분석 input_tag 함수는 attack_vector.py에서 사용하는 함수
        response_body = packet["response"]["body"]
        tag_list, tag_name_list, attack_vector, action_page, action_type, impactRate = inputTag(response_body, http_method, infor_vector)

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

        # robots.txt check
        if robots_result == True:
            attack_vector["misc"]["robots.txt"] = robots_result
        else:
            attack_vector["misc"].pop("robots.txt")

        # Error Page check
        if error_result == True:
            attack_vector["misc"]["error"] = error_result
        else:
            attack_vector["misc"].pop("error")

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
        print("attackvector", attack_vector)
        attack_vector["url"] = packet["request"]["full_url"]
        crx.append(attack_vector)

    Domain().PostDomain(json.dumps(data))
    return crx