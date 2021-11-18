from bs4 import BeautifulSoup
import requests, json, re, base64
from urllib.parse import urlparse

from requests import api

from Crawling.feature import func


def attackHeader(target_url):
    dict_data = requests.get(target_url, verify=False).headers
    infor_data = ""
    infor_vector = ""
    try:
        http_method = requests.options(target_url).headers['Allow'].replace(",", "").split(" ")
    except KeyError:
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
    attack_vector = dict() #list()
    data = dict()
    impactRate = 0

    text = soup.find_all('input')
    form = soup.find_all('form')

    with open("./attack_vector.json", 'r', encoding='UTF8') as f:
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
            except KeyError:
                continue
            if tag.attrs['type'] != "submit" and len(text) != 0:
                tag_list.append(base64.b64encode(str(tag).encode('utf-8')).decode('utf-8'))  # input tag 값 ex) <input ~
                try:
                    tag_name_list.append(tag.attrs['name'].replace("'", "").replace("+", "").replace("\"", ""))
                except:
                    pass

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

                if "board" in data["doubt"]["SQL injection"]["type"] or "board" in data["doubt"]["XSS"]["type"] \
                        or "account" in data["doubt"]["SQL injection"]["type"] or "account" in data["doubt"]["XSS"]["type"] \
                        or "None" in data["doubt"]["SQL injection"]["type"] or "None" in data["doubt"]["XSS"]["type"]:
                    pass
                else:
                    data["doubt"]["SQL injection"]["type"].append("None")
                    data["doubt"]["XSS"]["type"].append("None")

                    impactRate = 1

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
                    #~~~~~~~~~~~~File Upload
                    if tag.attrs['type'] == "file":
                        data["doubt"]["File Upload"] = True

                        impactRate = 2
                    else:
                        data["doubt"].pop("File Upload")
                except:
                    if "File Upload" in data["doubt"]:
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
    patterns = [    "s3\.[a-zA-Z0-9.-]+\.com",
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

def robotsTxt(url):
    # 주요정보통신기반시설_기술적_취약점_분석_평가_방법_상세가이드.pdf [page 726] robots.txt not set
    url = url.split("/")[0] + "//" + url.split("/")[2] + "/robots.txt"
    return True if "user-agent" not in requests.get(url).text.lower() or 404 == requests.get(url).status_code else False

def errorPage(url):
    # 주요정보통신기반시설_기술적_취약점_뿐석_평가_방법_상세가이드.pdf [page 678] Error Page not set
    url = url.split("/")[0] + "//" + url.split("/")[2] + "/BWASP/BWASP.TOP9"
    return True if 404 == requests.get(url).status_code and "not found" in requests.get(url).text.lower() else False

def directoryIndexing(target_url):
    return_data = list()
    api_key = func.apiKeyLoad()
    
    if api_key == False:
        print("[!] API 키가 없습니다.")
        return return_data

    GOOGLE_ENGINE_ID = api_key["google"]["google_search_api"]["engine_id"]
    GOOGLE_SEARCH_API = api_key["google"]["google_search_api"]["api"]

    target_domain = urlparse(target_url).netloc
    query = 'intitle:"Index Of" inurl:"{target_domain}"'.format(target_domain=target_domain)
    api_url = "https://customsearch.googleapis.com/customsearch/v1?cx={GOOGLE_ENGINE_ID}&key={GOOGLE_SEARCH_API}&q={QUERY}".format(GOOGLE_ENGINE_ID=GOOGLE_ENGINE_ID, GOOGLE_SEARCH_API=GOOGLE_SEARCH_API, QUERY=query)

    res = requests.get(api_url)

    if res.status_code == 200:
        api_result = res.json()
        if "items" not in api_result.keys():
            print("[*] No search data.")
            return return_data

        search_result = api_result["items"]
        
        for item in search_result:
            if item["title"].find("Index") != 0:
                continue

            return_data.append({
                "title": item["title"],
                "link": item["link"]
            })
    else:
        print("[!] API State_code: {}".format(res.status_code))
        print("[!] Please check API response.")
        # print("Print response: {}".format(res.text))

    return return_data

def adminPage(target_url):
    api_key = func.apiKeyLoad()
    return_data = list()
    target_domain = urlparse(target_url).netloc

    if api_key == False:
        print("[!] API 키가 없습니다.")
        return return_data
    
    GOOGLE_ENGINE_ID = api_key["google"]["google_search_api"]["engine_id"]
    GOOGLE_SEARCH_API = api_key["google"]["google_search_api"]["api"]

    f = open("./Crawling/directory.json")
    directory_list = json.load(f)

    for key in directory_list.keys():
        if "all" != key:
            continue
        inurl_list = list()
        for directory in directory_list[key]:
            inurl_list.append("inurl:{}".format(directory))

        query = 'site:{DOMAIN} AND ({INURL_LIST})'.format(DOMAIN=target_domain, INURL_LIST=" | ".join(inurl_list))
        api_url = "https://customsearch.googleapis.com/customsearch/v1?cx={GOOGLE_ENGINE_ID}&key={GOOGLE_SEARCH_API}&q={QUERY}".format(GOOGLE_ENGINE_ID=GOOGLE_ENGINE_ID, GOOGLE_SEARCH_API=GOOGLE_SEARCH_API, QUERY=query)
        # print(api_url)
        res = requests.get(api_url)
        if res.status_code == 200:
            api_result = res.json()
            if "items" not in api_result.keys():
                print("[*] No search data.")
                continue
            else:
                search_result = api_result["items"]
                for item in search_result:
                    return_data.append({
                        "title" : item["title"],
                        "link": item["link"]
                    })
        else:
            print("[!] API server error.")
            # print(res.json())
    
    return return_data

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
