import json
import re
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from multiprocessing import Lock
import os
import platform

from Crawling.feature import func


# Main Function


def loadCategory_meta():
    file = "./Crawling/wappalyzer/categories.json"
    f = open(file, "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    return data


def loadCategory(category):
    return_data = {}

    for name in "abcdefghijklmnopqrstuvwxyz_":
        file = "./Crawling/wappalyzer/{}.json".format(name)

        f = open(file, "r", encoding="utf-8")
        data = json.load(f)
        f.close()

        for key in data.keys():
            for cat in category:
                if cat in data[key]["cats"]:
                    return_data[key] = data[key]

    return return_data


def start(detect_list, lock, url, cur_page_links, current_url, req_res_packets, packet_indexes_, options):
    global data
    global cat_meta
    global packet_indexes

    category = list(range(1, 97))

    data = loadCategory(category)
    cat_meta = loadCategory_meta()
    packet_indexes = packet_indexes_[:]

    # detect_list

    # TODO: 이미 찾은 패킷은 더 이상 진행 x, detect 들 append 호출 했을 때 리턴값으로 구분 하면 가능
    for i, packet in enumerate(req_res_packets):
        if func.isExistExtension(packet["request"]["full_url"], ["image", "style", "font"]):
            continue
        for app in data:
            cats = cat_meta[str(retCatrepresnt(data[app]['cats']))]["name"]
            for option in options:
                if option['name'] == app:
                    appendResult(detect_list, lock, cats, app, "option", option['version'], 0, 0)
                    continue

            # 이미 탐지한 app일 때
            if cats in detect_list[0] and app in detect_list[0][cats]:
                # version 까지 획득했다면 더 이상 조회 x 
                if detect_list[0][cats][app]["version"] != 0:
                    continue

            # Including external domain as well as including same domain
            if not func.isSameDomain(url, packet["request"]["full_url"]):
                if "scripts" in list(data[app].keys()):
                    detectScripts(detect_list, lock, cur_page_links, data, cats, app)

                if "website" in list(data[app].keys()):
                    detectWebsite(detect_list, lock, cur_page_links, data, cats, app)
            else:
                if current_url == packet["request"]["full_url"]:  # 좋은 한정 범위 있다면 수정 ,현재 페이지 소스, google anayltics가 빠져 0 페이지가 현재 소스
                    if "html" in list(data[app].keys()):
                        detectHtml(detect_list, lock, packet, data, i, cats, app)

                    if "meta" in list(data[app].keys()):
                        detectMeta(detect_list, lock, packet, data, i, cats, app)

                    if "dom" in list(data[app].keys()):
                        detectDom(detect_list, lock, packet, data, i, cats, app)

                    if "url" in list(data[app].keys()):
                        detectUrl(detect_list, lock, url, cur_page_links, data, cats, app)

                if "headers" in list(data[app].keys()):
                    detectHeaders(detect_list, lock, packet, data, i, cats, app)

                if "cookies" in list(data[app].keys()):
                    detectCookies(detect_list, lock, packet, data, i, cats, app)
                    
    # return detect_list


def retCatrepresnt(cats):
    if len(cats) == 1:
        return cats[0]

    cats = sorted(cats)
    max_priority = -1

    for eachcat in cats:
        if cat_meta[str(eachcat)]['priority'] > max_priority:
            max_priority = cat_meta[str(eachcat)]['priority']
            cat_represent = eachcat

    return cat_represent


def initResult(detect_list, cats, app):
    detect_temp = detect_list[0]

    if cats not in detect_temp:
        # detect_list[0][cats]=dict()
        detect_temp[cats] = dict()

    if app not in detect_temp[cats]:
        detect_temp[cats][app] = dict()
        detect_temp[cats][app]["detect"] = list()
        detect_temp[cats][app]["version"] = 0
        detect_temp[cats][app]["request"] = list()
        detect_temp[cats][app]["response"] = list()
        detect_temp[cats][app]["url"] = list()
        detect_temp[cats][app]["icon"] = ""

    detect_list[0] = detect_temp


def retRelatedpacketidx(index):
    global packet_indexes

    if index == -1:
        return 0
    else:
        return packet_indexes[index]


# requset_index , reseponse_index 가 -1 이면 관련있는 index가 없다는 걸 의미, 0이면 현재 페이지 소스
def appendResult(detect_list, lock, cats, app, detectype, version, request_index=-1, response_index=-1, url=""):
    lock.acquire()

    if cats in detect_list[0] and app in detect_list[0][cats]:
        # version 까지 획득했다면 더 이상 조회 x 
        if detect_list[0][cats][app]["version"] != 0:
            return lock.release()
        else:
            if version == 0:
                return lock.release()

    request_index = retRelatedpacketidx(request_index)
    response_index = retRelatedpacketidx(response_index)
    initResult(detect_list, cats, app)
    detect_temp = detect_list[0]

    if detectype and detectype not in detect_temp[cats][app]["detect"]:
        detect_temp[cats][app]["detect"] = detectype
        # detect_temp[cats][app]["detect"].append(detectype)

    if version != 0 and detect_temp[cats][app]["version"] == 0:
        detect_temp[cats][app]["version"] = version

    if request_index and request_index not in detect_temp[cats][app]["request"]:
        detect_temp[cats][app]["request"].append(request_index)

    if response_index and response_index not in detect_temp[cats][app]["response"]:
        detect_temp[cats][app]["response"].append(response_index)

    if url and url not in detect_temp[cats][app]["url"]:
        detect_temp[cats][app]["url"].append(url)

    if "icon" in data[app].keys():
        if detect_temp[cats][app]["icon"] == "":
            detect_temp[cats][app]["icon"] = data[app]["icon"]

    detect_list[0] = detect_temp

    return lock.release()


# detect_list , app(이름) , request 패킷번호 ,response 패킷 번호
def appendImplies(detect_list, lock, app, request_index=-1, response_index=-1, url=""):
    if "implies" in data[app].keys():
        implies_list = data[app]["implies"]

        if type(implies_list) is str:
            implies_split = implies_list.split('\\;')
            implies_list = implies_split[0]
            appendResult(detect_list, lock, cat_meta[str(retCatrepresnt(data[implies_list]["cats"]))]["name"], implies_list, "implies", 0, request_index, response_index)
        else:
            for implies_line in implies_list:
                implies_split = implies_line.split('\\;')
                implies_line = implies_split[0]
                appendResult(detect_list, lock, cat_meta[str(retCatrepresnt(data[implies_line]["cats"]))]["name"], implies_line, "implies", 0, request_index, response_index)


# check response Header
def detectHeaders(detect_list, lock, packet, data, index, cats, app):
    for header in list(data[app]["headers"].keys()):
        if not header.lower() in list(packet["response"]["headers"].keys()):
            continue

        regex = data[app]["headers"][header]
        pattern = re.compile(regex.split("\\;")[0], re.I)
        regex_result = pattern.search(packet["response"]["headers"][header.lower()])

        if regex_result:
            version = detectVersion(regex, regex_result)
            appendResult(detect_list, lock, cats, app, "headers", version, -1, index)
            appendImplies(detect_list, lock, app, -1, index)


def detectHtml(detect_list, lock, packet, data, index, cats, app):
    if type(data[app]["html"]) == str:
        regex = data[app]["html"]
        pattern = re.compile(regex.split("\\;")[0], re.I)
        regex_result = pattern.search(packet["response"]["body"])
        if regex_result:
            version = detectVersion(regex, regex_result)
            appendResult(detect_list, lock, cats, app, "html", version, -1, index)
            appendImplies(detect_list, lock, app, -1, index)
    else:
        for regex in data[app]["html"]:
            pattern = re.compile(regex.split("\\;")[0], re.I)
            regex_result = pattern.search(packet["response"]["body"])
            if regex_result:
                version = detectVersion(regex, regex_result)
                appendResult(detect_list, lock, cats, app, "html", version, -1, index)
                appendImplies(detect_list, lock, app, -1, index)


def detectCookies(detect_list, lock, packet, data, index, cats, app):
    cookies = dict()
    # cookie에서 버전있는 경우는 한가지 CodeIgniter , ci_csrf_token
    version = 0
    if "cookie" not in list(packet["request"]["headers"].keys()):
        return

    for i in packet["request"]["headers"]["cookie"].split('; '):
        cookies[i.split('=')[0]] = i.split('=')[1]

    for cookie in data[app]["cookies"]:
        if cookie in cookies.keys():
            appendResult(detect_list, lock, cats, app, "cookies", version, index, -1)
            appendImplies(detect_list, lock, app, index, -1)
            # result = {"detect":["cookies"], "version":"False", "request":[index], "response":[], "url":[]}


def detectUrl(detect_list, lock, target_url, cur_page_links, data, cats, app):
    # version false 이유 : url은 \\;version 없음
    version = 0
    for url in cur_page_links:
        url_part = urlparse(url)
        url_comp = urlunparse(url_part._replace(params="", query="", fragment=""))

        if func.isSameDomain(target_url, url):
            if type(data[app]["url"]) == str:
                regex = data[app]["url"]
                pattern = re.compile(data[app]["url"].split('\\;')[0], re.I)
                regex_result = pattern.search(url_comp)

                if regex_result:
                    version = detectVersion(regex, regex_result)
                    appendResult(detect_list, lock, cats, app, "url", version, -1, -1, url)
                    appendImplies(detect_list, lock, app, -1, 0)
                    return
            else:
                for url_regex in data[app]["url"]:
                    pattern = re.compile(url_regex.split('\\;')[0], re.I)
                    regex_result = pattern.search(url_comp)

                    if regex_result:
                        version = detectVersion(url_regex, regex_result)
                        appendResult(detect_list, lock, cats, app, "url", version, -1, -1, url)
                        appendImplies(detect_list, lock, app, -1, 0)
                        return


def detectScripts(detect_list, lock, cur_page_links, data, cats, app):
    for url in cur_page_links:
        if type(data[app]["scripts"]) == str:
            regex = data[app]["scripts"]
            pattern = re.compile(data[app]["scripts"].split('\\;')[0], re.I)
            regex_result = pattern.search(url)

            if regex_result:
                version = detectVersion(regex, regex_result)
                appendResult(detect_list, lock, cats, app, "scripts", version, -1, 0, url)
                appendImplies(detect_list, lock, app, -1, 0)
                return
        else:
            for url_regex in data[app]["scripts"]:
                pattern = re.compile(url_regex.split('\\;')[0], re.I)
                regex_result = pattern.search(url)

                if regex_result:
                    version = detectVersion(url_regex, regex_result)
                    appendResult(detect_list, lock, cats, app, "scripts", version, -1, 0, url)
                    appendImplies(detect_list, lock, app, -1, 0)
                    return


def detectWebsite(detect_list, lock, cur_page_links, data, cats, app):
    version = 0
    # version 비어 있는 문제
    for url in cur_page_links:
        if type(data[app]["website"]) == str:
            if data[app]["website"] in url:
                # 1 => 현재 페이지
                appendResult(detect_list, lock, cats, app, "website", version, -1, 0, url)
                appendImplies(detect_list, lock, app, -1, 0)
                return
        else:
            for url_cond in data[app]["website"]:
                if url_cond in url:
                    # 1 => 현재 페이지
                    appendResult(detect_list, lock, cats, app, "website", version, -1, 0, url)
                    appendImplies(detect_list, lock, app, -1, 0)
                    return


def detectMeta(detect_list, lock, packet, data, index, cats, app):
    version = 0
    html = BeautifulSoup(packet["response"]["body"], features="html.parser")
    for meta_regex in data[app]["meta"].values():
        try:
            pattern = re.compile(meta_regex.split('\\;')[0],re.I)
        except: 
            pattern = re.compile("DonotD!ete!ct")
        meta_tag = html.find("meta", {"name":data[app]["meta"].keys()})

        if meta_tag and meta_tag.has_attr("content"):
            regex_result = pattern.search(meta_tag['content'])
            if regex_result:
                version = detectVersion(meta_regex, regex_result)
                appendResult(detect_list, lock, cats, app, "meta", version, -1, index)
                appendImplies(detect_list, lock, app, -1, index)


def detectDom(detect_list, lock, packet, data, index, cats, app):
    if "dom" in data[app].keys():
        if type(data[app]["dom"]) is dict:  # dict 인지 확인
            for key_name in list(data[app]["dom"].keys()):
                html = BeautifulSoup(packet["response"]["body"], features="html.parser")
                temps = html.select(key_name)
                if (temps):
                    for subkey_name in list(data[app]["dom"][key_name].keys()):
                        if subkey_name == "attributes" or subkey_name == "properties":
                            for temp in temps:
                                if subkey_name in temp.attrs:
                                    regex = data[app]["dom"][key_name][subkey_name]
                                    regex_results = re.match(regex.split('\\;')[0], temp[subkey_name], re.I)
                                    if regex_results:
                                        version = detectVersion(regex, regex_results)
                                        appendResult(detect_list, lock, cats, app, "dom", version, -1, index)
                                        appendImplies(detect_list, lock, app, -1, index)

                        if subkey_name == "text":
                            regex = data[app]["dom"][key_name]["text"]
                            pattern = data[app]["dom"][key_name]["text"].split('\\;')[0]

                            for temp in temps:
                                try:
                                    regex_results = re.match(pattern, temp.getText(), re.I)
                                except:
                                    pattern = pattern.replace("\w-", "-\w")
                                    regex_results = re.match(pattern, temp.getText(), re.I)

                                if regex_results:
                                    version = detectVersion(regex, regex_results)
                                    appendResult(detect_list, lock, cats, app, "dom", version, -1, index)
                                    appendImplies(detect_list, lock, app, -1, index)
                                    # match 값 존재하면 넣기

                        if subkey_name == "exists":
                            appendResult(detect_list, lock, cats, app, "dom", 0, -1, index)
                            appendImplies(detect_list, lock, app, -1, index)

                        if subkey_name == "src":
                            for temp in temps:
                                if "src" in temp.attrs:
                                    regex = data[app]["dom"][key_name]["src"]
                                    regex_results = re.match(regex.split('\\;')[0], temp['src'], re.I)
                                    if regex_results:
                                        version = detectVersion(regex, regex_results)
                                        appendResult(detect_list, lock, cats, app, "dom", version, -1, index)
                                        appendImplies(detect_list, lock, app, -1, index)
                        # if key_name == "properties" 아직 구현 x, 2가지만 해당됨
                        # 일단은 properties는 name과 같은 느낌이라 생각 , attrs로 존재 여무 확인
                        # 아직은 dict 구조지만 값은 비교안함 

            # dictionary 형태가 아니라 단일 값으로 존재할 때

        elif type(data[app]["dom"]) is list:
            html = BeautifulSoup(packet["response"]["body"], features="html.parser")

            for line_list in data[app]["dom"]:
                if html.select(line_list):
                    appendResult(detect_list, lock, cats, app, "dom", 0, -1, index)
                    appendImplies(detect_list, lock, app, -1, index)

        elif type(data[app]["dom"]) is str:
            html = BeautifulSoup(packet["response"]["body"], features="html.parser")

            if html.select(data[app]["dom"]):
                appendResult(detect_list, lock, cats, app, "dom", 0, -1, index)
                appendImplies(detect_list, lock, app, -1, index)


def detectVersion(regex, regex_results, type="search"):
    version = ""
    version_group = False
    result = regex.split('\\;')

    if "\\;version" not in regex:
        return 0

    if len(result) > 1:
        for result_line in result[1:]:
            if "version:" in result_line:
                # version:1 version:\\1
                version_group = result_line[8:]
                break

        # TODO: if "version_group is not False" or "version_group is True" or "version_group"
        if version_group != False:
            if type == "findall":
                pass

            if type in ["match", "search"]:
                # groups로 가져오면 findall 처럼 0 부터 regex 그룹과 매칭 됨
                regex_results = regex_results.groups()

            version_regex = '([^\\\\]*)(?:\\\\)?([^\?]*)\??([^:]*):?(.*)$'
            version_group = re.match(version_regex, version_group).groups()

            if version_group[2] or version_group[3]:
                if regex_results[int(version_group[1]) - 1]:
                    if "\\" in version_group[2]:
                        version = regex_results[int(version_group[2].replace("\\", "")) - 1]
                    else:
                        version = version_group[2]

                else:
                    if "\\" in version_group[3]:
                        version = regex_results[int(version_group[3].replace("\\", "")) - 1]
                    else:
                        version = version_group[3]

            else:
                version = regex_results[int(version_group[1]) - 1]

            version = str(version) + str(version_group[0])
            version = re.sub("[^0-9\.]", "", str(version))

    if not version:
        version = 0
        
    return version


def getSubdomain(target: str) -> dict:
    """ Get subdoamin list from target.

    You can call this function like the code below.
    `getSubdomain('http://blog.naver.com')` or `getSubdomain('blog.naver.com/this/is/path')`.
    Return dictionary type including subdomain list or error.
    - success: {
        "result" : "success",
        "data" : ["m.blog.naver.com", "upload.blog.naver.com", ...]
    }
    - error: {
        "result" : "error",
        "message" : "[Error info] [Error detail]"
    }
    
    Args:
        - target: Value of target's url or host.
    Returns:
        - Return dict type data.
    """

    def run(binary_name: str, netloc: str) -> dict:
        try:
            data = os.popen(f"./assets/{binary_name} -subs-only {netloc}").read()
            data = list(set(data.split("\n")))
            result = list()

            for d in data:
                if len(d) == 0 or d == netloc:
                    continue
                result.append(d)

            return {
                "result" : "success",
                "data" : result
            }

        except Exception as e:
            return {
                "result" : "error",
                "message" : e
            }


    try:
        netloc = urlparse(target).netloc
        netloc = re.sub("`|\$|{|}|;|\||&|%", "", netloc, flags=re.MULTILINE)
        os_info = platform.system()
        result = dict()

        if not netloc or len(netloc) == 0:
            return {
                "result" : "error",
                "message" : "Host를 다시 확인해 주세요."
            }
        
        if os_info == "Linux":
            result = run("assetfinder", netloc)
        elif os_info == "Windows":
            result = run("assetfinder.exe", netloc)
        else:
            return {
                "result" : "error",
                "message" : "해당 기능은 Linux, Windows에서만 제공됩니다."
            }
        
        if result["result"] == "success":
            return result
        else:
            return {
                "result" : "error",
                "message" : "subdomain 기능에서 에러가 발생했습니다. " + str(result["message"])
            }

    
    except Exception as e:
        print("[!] Get Subdomain Error: ", e)
        return {
            "result" : "error",
            "message" : "예기치 못한 에러가 발생했습니다. " + str(e)
        }