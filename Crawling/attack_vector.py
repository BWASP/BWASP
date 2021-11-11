from bs4 import BeautifulSoup
import requests
import json
import re


def attack_header(target_url):
    r = requests.get(target_url, verify=False)
    dict_data = r.headers
    infor_data = ""
    infor_vector = ""
    try:
        http_method = requests.options(target_url).headers['Allow'].replace(",", "").split(" ")
    except:
        http_method = "private"

    try:
        tmp_data = dict_data['Set-Cookie']
        i = len(tmp_data.split())
        if "HttpOnly" in tmp_data:
            for j in range(0, i):
                infor_data += tmp_data.split()[j] + "\n"
        elif "Secure" in tmp_data:
            for j in range(0, i):
                infor_data += tmp_data.split()[j] + "\n"
        else:
            infor_data = tmp_data
            infor_vector += "Not_HttpOnly\n"

    except:
        infor_vector += "Not_HttpOnly\n"

    try:
        tmp_data = dict_data['X-Frame-Options']
        i = len(tmp_data.split())
        for j in range(0, i):
            infor_data += tmp_data.split()[j] + "\n"

    except:
        infor_vector += "Not_X-Frame-Options\n"

    return http_method, infor_vector


def input_tag(response_body, http_method, infor_vector):
    # form tag action and input tag and input name parse
    soup = BeautifulSoup(response_body, 'html.parser')

    tag_list = list()
    tag_name_list = list()
    action_page = list()
    action_type = list()

    attack_vector = dict() #list()

    data = dict()

    impactRate = 0

    text = soup.find_all('input')
    form = soup.find_all('form')

    with open("./attack_vector.json", 'r', encoding='UTF8') as f:
        data = json.load(f)

    for tag in text:
        try:
            if tag.attrs['type'] != "submit" and len(text) != 0:
                tag_list.append(str(tag))  # input tag 값 ex) <input ~
                tag_name_list.append(tag.attrs['name'])

                #~~~~~~~~~~~~SQL Injection and XSS

                # th tag check (board) and type="password" check (login)
                if "<th" in response_body:
                    if "None" in data["doubt"]["SQL injection"]["type"] or "None" in data["doubt"]["XSS"]["type"]:
                        index_sql = data["doubt"]["SQL injection"]["type"].index("None")
                        index_xss = data["doubt"]["XSS"]["type"].index("None")
                        del (data["doubt"]["SQL injection"]["type"][index_sql])
                        del (data["doubt"]["XSS"]["type"][index_xss])

                    if "board" in data["doubt"]["SQL injection"]["type"] or "board" in data["doubt"]["XSS"]["type"]:
                        pass
                    else:
                        data["doubt"]["SQL injection"]["type"].append("board")
                        data["doubt"]["XSS"]["type"].append("board")

                        impactRate = 2

                if tag.attrs['type'] == "password":
                    if "None" in data["doubt"]["SQL injection"]["type"] or "None" in data["doubt"]["XSS"]["type"]:
                        index_sql = data["doubt"]["SQL injection"]["type"].index("None")
                        index_xss = data["doubt"]["XSS"]["type"].index("None")
                        del (data["doubt"]["SQL injection"]["type"][index_sql])
                        del (data["doubt"]["XSS"]["type"][index_xss])

                    if "account" in data["doubt"]["SQL injection"]["type"] or "account" in data["doubt"]["XSS"]["type"]:
                        pass
                    else:
                        data["doubt"]["SQL injection"]["type"].append("account")
                        data["doubt"]["XSS"]["type"].append("account")

                        impactRate = 2

                if "board" in data["doubt"]["SQL injection"]["type"] or "board" in data["doubt"]["XSS"]["type"] \
                        or "account" in data["doubt"]["SQL injection"]["type"] or "account" in data["doubt"]["XSS"]["type"] \
                        or "None" in data["doubt"]["SQL injection"]["type"] or "None" in data["doubt"]["XSS"]["type"]:
                    pass
                else:
                    data["doubt"]["SQL injection"]["type"].append("None")
                    data["doubt"]["XSS"]["type"].append("None")

                    impactRate = 1

                if "Not_HttpOnly" in infor_vector:
                    data["doubt"]["XSS"]["header"]["HttpOnly"] = True

                    if impactRate != 2:
                        impactRate = 1

                if "Not_X-Frame-Options" in infor_vector:
                    data["doubt"]["XSS"]["header"]["X-Frame-Options"] = True

                    if impactRate != 2:
                        impactRate = 1

                #~~~~~~~~~~~~Allow Method
                if "private" not in http_method:
                    data["info"]["allowMethod"] = http_method

                #~~~~~~~~~~~~File Upload
                if tag.attrs['type'] == "file":
                    data["doubt"]["File Upload"] = True

                    impactRate = 2

        except:
            pass

        attack_vector = data

    if form:
        for tag in form:
            try:
                action_page.append(tag.attrs['action'])
            except:
                action_page.append("None")
            try:
                action_type.append(tag.attrs['method'])
            except:
                action_type.append("None")

    return tag_list, tag_name_list, attack_vector, action_page, action_type, impactRate


def corsCheck(packet):
    cors_check = "None"

    response_header = packet["response"]["headers"]

    try:
        if response_header['access-control-allow-origin'] == "*":
            cors_check = "CORS Misconfiguration: *"
    except:
        pass

    return cors_check

def openRedirectionCheck(packet):
    try:
        if packet["open_redirect"]:
            return packet["request"]["full_url"]
    except:
        return ""

def s3BucketCheck(packet):
    return_s3_url = []
    patterns = [    "[a-z0-9.-]+\.s3\.amazonaws\.com[\/]?",
                    "[a-z0-9.-]+\.s3-[a-z0-9-]\.amazonaws\.com[\/]?",
                    "[a-z0-9.-]+\.s3-website[.-](eu|ap|us|ca|sa|cn)",
                    "[\/\/]?s3\.amazonaws\.com\/[a-z0-9._-]+",
                    "[\/\/]?s3-[a-z0-9-]+\.amazonaws\.com/[a-z0-9._-]+",
                    "[a-z0-9-]+\.s3-[a-z0-9-]+\.amazonaws\.com/[a-z0-9._-]+",
                    "[a-z0-9-]+\.s3-[a-z0-9-]+\.amazonaws\.com[\/]?",
                    "[a-z0-9\.\-]{3,63}\.s3[\.-](eu|ap|us|ca|sa)-\w{2,14}-\d{1,2}\.amazonaws.com[\/]?",
                    "[a-z0-9\.\-]{0,63}\.?s3.amazonaws\.com[\/]?",
                    "[a-z0-9\.\-]{3,63}\.s3-website[\.-](eu|ap|us|ca|sa|cn)-\w{2,14}-\d{1,2}\.amazonaws.com[\/]?"]

    for pattern in patterns:
        regex = re.compile(pattern)
        res_body = regex.findall(packet["request"]["body"])
        req_body = regex.findall(packet["response"]["body"])

        if res_body:
            return_s3_url += res_body
        if req_body:
            return_s3_url += req_body

    print(list(set(return_s3_url)))
    input()
    return list(set(return_s3_url))

def jwtCheck(packet):
    return_jwt = []
    patterns = ["^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"]

    for pattern in patterns:
        regex = re.compile(pattern)
        req_header = []
        req_body = []
        res_header = []
        res_body = []

        for header_key in packet["request"]["headers"].keys():
            req_header += regex.findall(packet["request"]["headers"][header_key])
        for header_key in packet["response"]["headers"].keys():
            res_header += regex.findall(packet["response"]["headers"][header_key])
        req_body = regex.findall(packet["request"]["body"])
        res_body = regex.findall(packet["response"]["body"])

        return_jwt += req_header + req_body + res_header + res_body

    print(list(set(return_jwt)))
    input()
    return list(set(return_jwt))

def robots_txt(url):
    # 주요정보통신기반시설_기술적_취약점_분석_평가_방법_상세가이드.pdf [page 726] robots.txt not set
    url = url.split("/")[0] + "//" + url.split("/")[2] + "/robots.txt"
    return True if "user-agent" not in requests.get(url).text.lower() or 404 == requests.get(url).status_code else False




# input tag 함수, Packets에서 불러오는 Cookie 값 + QueryString(Parameter) JSON 형태 예시 -> domain 테이블 Details 컬럼
"""
{
  "tag": [
    "tag A",
    "tag B"
  ],
  "cookie": {
    "PHPSESSID": "8a7s6f89sd6fg98f6s98d",
    "JSESSIONID": "abcdefghijklmnop"
  },
  "queryString": {
    "hello": "world"
  }
}

?hello=world
"""
