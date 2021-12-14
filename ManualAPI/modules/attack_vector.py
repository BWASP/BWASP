from bs4 import BeautifulSoup
import requests, json, re, base64, sys, os
from Crawling.feature.keywordCmp import keywordCmp
from urllib.parse import urlparse
from modules import func
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def attackHeader(target_url):
    dict_data = requests.get(target_url, verify=False).headers
    infor_data = ""
    infor_vector = ""
    try:
        http_method = requests.options(target_url, verify=False).headers['Allow'].replace(",", "").split(" ")
    except: #KeyError or ConnectionError
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


def inputTag(response_body, http_method, infor_vector):
    # form tag action and input tag and input name parse
    try:
        soup = BeautifulSoup(response_body, 'html.parser')
    except:
        soup = BeautifulSoup("", 'html.parser')

    tag_list = list()
    tag_name_list = list()
    action_page = list()
    action_type = list()
    attack_vector = dict()  # list()
    data = dict()
    impactRate = 0
    check = 0
    cmp_sql_check = False
    cmp_sql_xss_check = False
    cmp_logic_check = False

    text = soup.find_all('input')
    form = soup.find_all('form')
    with open("./ManualAPI/modules/attack_vector.json", 'r', encoding='UTF8') as f:
        data = json.load(f)

    # ~~~~~~~~~~~~Allow Method
    if "private" not in http_method:
        data["info"]["allowMethod"] = http_method
    else:
        data["info"].pop("allowMethod")

    if len(text) != 0:
        for tag in text:
            try:
                if tag.attrs['type']:
                    pass
            except: #KeyError
                continue
            if tag.attrs['type'] != "submit" and len(text) != 0 and tag.attrs['type'] != "checkbox":
                tag_list.append(base64.b64encode(str(tag).encode('utf-8')).decode('utf-8'))  # input tag 값 ex) <input ~
                try:
                    tag_name_list.append(tag.attrs['name'].replace("'", "").replace("+", "").replace("\"", ""))
                except:
                    pass

                # ~~~~~~~~~~~~SQL Injection and XSS

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

                try:
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
                except:
                    pass

                cmp_sql_check = keywordCmp().keywordCmp_SQL(tag_name_list, cmp_sql_check)
                cmp_sql_xss_check = keywordCmp().keywordCmp_SQL_XSS(tag_name_list, cmp_sql_xss_check)
                cmp_logic_check = keywordCmp().keywordCmp_Logic(tag_name_list, cmp_logic_check)

                if "board" in data["doubt"]["SQL injection"]["type"] or "board" in data["doubt"]["XSS"]["type"] \
                        or "account" in data["doubt"]["SQL injection"]["type"] or "account" in data["doubt"]["XSS"][
                    "type"] \
                        or "None" in data["doubt"]["SQL injection"]["type"] or "None" in data["doubt"]["XSS"]["type"]:
                    pass
                elif cmp_sql_check:
                    data["doubt"]["SQL injection"]["type"].append("None")

                    impactRate = 1
                elif cmp_sql_xss_check:
                    data["doubt"]["SQL injection"]["type"].append("None")
                    data["doubt"]["XSS"]["type"].append("None")

                    impactRate = 1
                elif cmp_logic_check:
                    data["doubt"]["Logic Flaw"] = True

                    impactRate = 1
                else:
                    if "SQL injection" in data["doubt"]:
                        pass
                    else:
                        data["doubt"]["Parameter"] = True

                        impactRate = 0

                if "Not_HttpOnly" in infor_vector:
                    if "HttpOnly" not in data["doubt"]["XSS"]["required"]:
                        data["doubt"]["XSS"]["required"].append("HttpOnly")

                    if impactRate != 2:
                        impactRate = 1

                if "Not_X-Frame-Options" in infor_vector:
                    if "X-Frame-Options" not in data["doubt"]["XSS"]["required"]:
                        data["doubt"]["XSS"]["required"].append("X-Frame-Options")

                    if impactRate != 2:
                        impactRate = 1

                try:
                    # ~~~~~~~~~~~~File Upload
                    if tag.attrs['type'] == "file":
                        data["doubt"]["File Upload"] = True
                        check = 2

                        impactRate = 2
                    else:
                        if check == 2:
                            pass
                        else:
                            check = 1
                except:
                    if "File Upload" in data["doubt"]:
                        data["doubt"].pop("File Upload")

        if check == 1:
            data["doubt"].pop("File Upload")

        attack_vector = data

    else:
        attack_vector = data
        try:
            attack_vector["doubt"].pop("SQL injection")
        except:
            pass
        try:
            attack_vector["doubt"].pop("XSS")
        except:
            pass
        try:
            attack_vector["doubt"].pop("File Upload")
        except:
            pass

    if form:
        for tag in form:
            try:
                action_page.append(base64.b64encode(tag.attrs['action'].encode('utf-8')).decode('utf-8'))
            except:
                pass
            try:
                action_type.append(base64.b64encode(tag.attrs['method'].encode('utf-8')).decode('utf-8'))
            except:
                pass

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
    patterns = ["s3\.[a-zA-Z0-9.-]+\.com",
                "[a-zA-Z0-9.-]+\.s3\.amazonaws\.com[\/]?[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9.-]+\.amazonaws\.com[\/]?[a-zA-Z0-9\-\/]*"
                "[a-zA-Z0-9.-]+\.s3-[a-zA-Z0-9-]\.amazonaws\.com[\/]?[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9.-]+\.s3-website[.-](?: eu|ap|us|ca|sa|cn)",
                "[\/\/]?s3\.amazonaws\.com\/[a-zA-Z0-9\-\/]*",
                "[\/\/]?s3-[a-z0-9-]+\.amazonaws\.com/[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9-]+\.s3-[a-zA-Z0-9-]+\.amazonaws\.com/[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9-]+\.s3-[a-zA-Z0-9-]+\.amazonaws\.com[\/]?[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9\.\-]{3,63}\.s3[\.-](?: eu|ap|us|ca|sa)-\w{2,14}-\d{1,2}\.amazonaws.com[\/]?[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9\.\-]{0,63}\.?s3.amazonaws\.com[\/]?[a-zA-Z0-9\-\/]*",
                "[a-zA-Z0-9\.\-]{3,63}\.s3-website[\.-](?: eu|ap|us|ca|sa|cn)-\w{2,14}-\d{1,2}\.amazonaws.com[\/]?[a-zA-Z0-9\-\/]*"]

    for pattern in patterns:
        regex = re.compile(pattern)
        res_body = regex.findall(packet["request"]["body"])
        req_body = regex.findall(packet["response"]["body"])

        if res_body:
            return_s3_url += res_body
        if req_body:
            return_s3_url += req_body

    return list(set(return_s3_url))


def jwtCheck(packet):
    return_jwt = []
    patterns = ["([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_=]+)\.([a-zA-Z0-9_\-\+\/=]*)"]

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
    return list(set(return_jwt))


def robotsTxt(current_url):
    # 주요정보통신기반시설_기술적_취약점_분석_평가_방법_상세가이드.pdf [page 726] robots.txt not set
    return True if "user-agent" not in requests.get(current_url, verify=False).text.lower() or 404 == requests.get(current_url, verify=False).status_code else False


def errorPage(current_url):
    # 주요정보통신기반시설_기술적_취약점_뿐석_평가_방법_상세가이드.pdf [page 678] Error Page not set
    return True if 404 == requests.get(current_url, verify=False).status_code and "not found" in requests.get(current_url, verify=False).text.lower() else False

def ReflectedXSSCheck(packet: dict, target_url: str) -> bool:
    if not func.isSameDomain(packet["request"]["full_url"], target_url):
        return False

    queries = urlparse(packet["request"]["full_url"]).query

    if queries:
        queries = queries.split("&")
        try:
            soup = BeautifulSoup(packet["response"]["body"], "html.parser")
        except:
            return False

        for query in queries:
            datas = query.split("=")

            if len(datas) != 2:
                break

            input_tag = soup.find("input", {"name": datas[0]})
            if input_tag and datas[1] == input_tag.get("value"):
                return True

    return False


def SSRFCheck(packet: dict) -> bool:
    if "open_redirect" in packet.keys():
        return False

    if packet["request"]["method"] == "GET":
        queries = urlparse(packet["request"]["full_url"]).query.split("&")
        for data in queries:
            datas = data.split("=")

            if len(datas) != 2:
                continue

            if func.isStringAnUrl(datas[1]):
                return True

    elif packet["request"]["method"] == "POST":
        body = packet["request"]["body"]
        pattern = "((?:http|ftp|https)(?:://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)"
        result = re.findall(pattern, body)

        if len(result) != 0:
            return True

    return False

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
