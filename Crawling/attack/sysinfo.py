import json
import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from Crawling.feature import func

# Main Function
#dom 에서 driver 사용 예정


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


def start(url, cur_page_links, req_res_packets, driver, options):
    category =  list(range(1,96))
    global data
    data = loadCategory(category)
    global cat_meta
    cat_meta=loadCategory_meta()
    detect_list = {}

    for i, packet in enumerate(req_res_packets):
        for app in data:
            cats = data[app]['cats']
            for option in options:
                if option['name'] == app:
                    appendResult(detect_list,cats,app,"option",option['version'],0,0)
                    continue
            # Including external domain as well as including same domain
            if not func.isSameDomain(url, packet["request"]["full_url"]):
                if "scripts" in list(data[app].keys()):
                    detectScripts(detect_list, cur_page_links, data, cats, app)
                if "website" in list(data[app].keys()):
                    detectWebsite(detect_list, cur_page_links, data, cats, app)
            else:
                if "url" in list(data[app].keys()):
                    detectUrl(detect_list, cur_page_links, data, cats, app)
                if "headers" in list(data[app].keys()):
                    detectHeaders(detect_list, packet, data, i, cats, app)
                if "html" in list(data[app].keys()):
                    detectHtml(detect_list, packet, data, i, cats, app)
                if "cookies" in list(data[app].keys()):
                    detectCookies(detect_list, packet, data, i, cats, app)
                if "meta" in list(data[app].keys()):
                    detectMeta(detect_list, packet, data, i, cats, app)
                # if "dom" in list(data[app].keys()):
                #     result = detectDom(data, driver, i, app)
                #     detect_list = resultFunc(detect_list, app, result)
#반환전 숫자 정렬 , 글자로 바꾸기 
    return detect_list

def retCatrepresnt(cats):
    if len(cats) == 1:
        return cats[0]
    cats = sorted(cats)
    max_priority=-1
    for eachcat in cats:
        #if cat_meta[str(eachcat)]['priority'] > max_priority:
        max_priority = cat_meta[str(eachcat)]['priority']
        cat_represent = eachcat
    
    return cat_represent



def initResult(detect_list,cats,app):  
    if cats not in detect_list.keys():
        detect_list[cats]=dict()
    
    if app not in detect_list[cats].keys():
        detect_list[cats][app]=dict()
        detect_list[cats][app]["detect"]=list()
        detect_list[cats][app]["version"]="false"
        detect_list[cats][app]["request"]=list()
        detect_list[cats][app]["response"]=list()
        detect_list[cats][app]["url"]=list()
        detect_list[cats][app]["icon"]="false"


# requset_index , reseponse_index 가 0 이면 관련있는 index가 없다는 걸 의미

def appendResult(detect_list,cats,app,detectype,version,request_index=0,response_index=0,url=""):

    cats = retCatrepresnt(cats) 
    initResult(detect_list,cats,app)
    if detectype and detectype not in detect_list[cats][app]["detect"]:
        detect_list[cats][app]["detect"].append(detectype)
    if version != "false" and detect_list[cats][app]["version"] == "false":
        detect_list[cats][app]["version"]=version
    if request_index and request_index not in detect_list[cats][app]["request"]:
        detect_list[cats][app]["request"].append(request_index)
    if response_index and response_index not in detect_list[cats][app]["response"]:
        detect_list[cats][app]["response"].append(response_index)
    if url and url not in detect_list[cats][app]["url"]:
        detect_list[cats][app]["url"].append(url)
    if "icon" in data[app].keys():
        if detect_list[cats][app]["icon"] == "false":
            detect_list[cats][app]["icon"] = data[app]["icon"]


# detect_list , app(이름) , request 패킷번호 ,response 패킷 번호 
def  appendImplies(detect_list,app,request_index=0,response_index=0,url=""):
    if "implies" in data[app].keys():
        implies_list=data[app]["implies"]

        if type(implies_list) is str:
            implies_split=implies_list.split('\\;')
            implies_list=implies_split[0]
            appendResult(detect_list,data[implies_list]["cats"],implies_list,"implies","false",request_index,response_index)
        else:
            for implies_line in	implies_list:
                implies_split=implies_line.split('\\;')
                implies_line=implies_split[0]
                appendResult(detect_list,data[implies_line]["cats"],implies_line,"implies","false",request_index,response_index)

# check response Header
def detectHeaders(detect_list,packet, data, index, cats, app):
    for header in list(data[app]["headers"].keys()):
        if not header.lower() in list(packet["response"]["headers"].keys()):
            continue

        regex = data[app]["headers"][header]
        pattern = re.compile(regex.split("\\;")[0])
        regex_result = pattern.search(packet["response"]["headers"][header.lower()])

        if regex_result:
            version = detectVersion(regex, regex_result)
            appendResult(detect_list,cats,app,"headers",version,0,index)
            appendImplies(detect_list,app,0,index)

def detectHtml(detect_list, packet, data, index, cats, app):
    if type(data[app]["html"]) == str:
        regex=data[app]["html"]
        pattern = re.compile(regex.split("\\;")[0])
        regex_result = pattern.search(packet["response"]["body"])
        if regex_result:
            version = detectVersion(regex, regex_result)
            appendResult(detect_list,cats,app,"html",version,0,index)
            appendImplies(detect_list,app,0,index)
    else:
        for regex in data[app]["html"]:
            pattern = re.compile(regex.split("\\;")[0])
            regex_result = pattern.search(packet["response"]["body"])
            if regex_result:
                version = detectVersion(regex, regex_result)
                appendResult(detect_list,cats,app,"html",version,0,index)
                appendImplies(detect_list,app,0,index)
                
    
    

def detectCookies(detect_list, packet, data, index, cats, app):
    cookies = dict()
    #fale? 쿠키에는 version 없는지 확인
    # cookie에서 버전있는 경우는 한가지
    version = "false"
    if "cookie" not in list(packet["request"]["headers"].keys()):
        return
    for i in packet["request"]["headers"]["cookie"].split('; '):
        cookies[i.split('=')[0]] = i.split('=')[1]
    for cookie in data[app]["cookies"]:
        if cookie in cookies.keys():
            appendResult(detect_list,cats,app,"cookies",version,index,0)
            appendImplies(detect_list,app,index,0)
            #result = {"detect":["cookies"], "version":"False", "request":[index], "response":[], "url":[]}

def detectUrl(detect_list, cur_page_links, data, cats, app):
    #version false 이유
    version ="false"
    for url in cur_page_links:
        if type(data[app]["url"]) == str:
            regex=data[app]["url"]
            pattern = re.compile(data[app]["url"].split('\\;')[0])
            regex_result = pattern.search(url)
            
            if regex_result:
                version = detectVersion(regex, regex_result)
                appendResult(detect_list,cats,app,"url",version,0,1,url)
                appendImplies(detect_list,app,0,1)
                return
        else:
            for url_regex in data[app]["url"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)

                if regex_result:
                    version = detectVersion(url_regex, regex_result)
                    appendResult(detect_list,cats,app,"url",version,0,1,url)
                    appendImplies(detect_list,app,0,1)
                    return
    

def detectScripts(detect_list, cur_page_links, data, cats, app):
    for url in cur_page_links:
        if type(data[app]["scripts"]) == str:
            regex=data[app]["scripts"]
            pattern = re.compile(data[app]["scripts"].split('\\;')[0])
            regex_result = pattern.search(url)
            if regex_result:
                version = detectVersion(regex, regex_result)
                appendResult(detect_list,cats,app,"scripts",version,0,1,url)
                appendImplies(detect_list,app,0,1)
                return
        else:
            for url_regex in data[app]["scripts"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)
                if regex_result:
                    version = detectVersion(url_regex,regex_result)
                    appendResult(detect_list,cats,app,"scripts",version,0,1,url)
                    appendImplies(detect_list,app,0,1)
                    return
    

def detectWebsite(detect_list, cur_page_links, data, cats, app):
    version="false"
     #version 비어 있는 문제
    for url in cur_page_links:
        if type(data[app]["website"]) == str:
            if data[app]["website"] in url:
                #1 => 현재 페이지
                appendResult(detect_list,cats,app,"website",version,0,1,url)
                appendImplies(detect_list,app,0,1)
                return
        else:
            for url_cond in data[app]["website"]:
                if url_cond in url:
                     #1 => 현재 페이지
                    appendResult(detect_list,cats,app,"website",version,0,1,url)
                    appendImplies(detect_list,app,0,1)
                    return

def detectMeta(detect_list, packet, data, index, cats, app):
    version="false"
    html = BeautifulSoup(packet["response"]["body"], features="html.parser")
    for meta_regex in data[app]["meta"].values():
        try:
            pattern = re.compile(meta_regex.split('\\;')[0])
        except: 
            pattern = "vmkwdlwkw"
        meta_tag = html.find("meta", {"name":data[app]["meta"].keys()})
        if meta_tag and meta_tag.has_attr("content"):
            regex_result = pattern.search(meta_tag['content'])
            if regex_result:
                version = detectVersion(meta_regex, regex_result)
                appendResult(detect_list,cats,app,"meta",version,0,index)
                appendImplies(detect_list,app,0,index)

'''
def detectMeta(detect_list, packet, data, index, cats, app):
    if "meta" in data[app].keys():
        html = BeautifulSoup(packet["response"]["body"], features="html.parser")
        metas = html.select('meta[name][content]')
        for meta_line in metas:             
            for comp_metakey in data[app]["meta"]:
                if meta_line['name'] != comp_metakey:
                    continue
                if type(data[app]["meta"][comp_metakey]) is list:
                    print("list type!!",data[app]["meta"][comp_metakey])
                    for comp_metakey in data[app]["meta"][comp_metakey]:
                        regex=comp_metakey
                        pattern = comp_metakey.split('\\;')[0]
                        regex_results=re.findall(pattern,meta_line["content"],re.I)
                        #현재 페이지는 response 패킷 1으로 침 
                        if(regex_results):
                            version = detectVersion(regex, regex_results)
                            appendResult(detect_list,cats,app,"meta",version,0,index)
                            appendImplies(detect_list,app,0,index)
                    else:
                        regex=data[app]["meta"][comp_metakey]
                        pattern = data[app]["meta"][comp_metakey].split('\\;')[0]
                        regex_results=re.findall(pattern,meta_line["content"],re.I)
                    #현재 페이지는 response 패킷 1으로 침 
                    if regex_results :
                        version = detectVersion(regex, regex_results)
                        appendResult(detect_list,cats,app,"meta",version,0,index)
                        appendImplies(detect_list,app,0,index)
'''
'''
def detectVersion(full_regex, detected_info):
    if "\\;version:\\" not in full_regex:
        return "False"
                
    version_pattern = re.compile('(\\d+(\\.)?)+')
    version_info = version_pattern.search(detected_info)
    
    if version_info:
        return version_info.group()
    else:
        return "False"
'''

def detectVersion(regex,regex_results,type="search"):
    version=""
    version_group="false"
    result = regex.split('\\;')
    if "\\;version" not in regex:
        return "false"
    if len(result) > 1: 
        for result_line in result[1:]:
            if "version:" in result_line:
                #version:1 version:\\1
                version_group=result_line[8:]
                break             
        if version_group != "false":  
            if type == "findall":
                pass
            if type in ["match","search"]:
                # groups로 가져오면 findall 처럼 0 부터 regex 그룹과 매칭 됨
                regex_results=regex_results.groups()
            version_regex = '([^\\\\]*)(?:\\\\)?([^\?]*)\??([^:]*):?(.*)$'
            version_group = re.match(version_regex,version_group).groups()
            if  (version_group[2] or version_group[3]):
                if regex_results[int(version_group[1])-1]:
                    if "\\" in version_group[2]:
                        version=regex_results[int(version_group[2].replace("\\",""))-1]
                    else:   
                        version=version_group[2]
                else:
                    if "\\" in version_group[3]:
                        version=regex_results[int(version_group[3].replace("\\",""))-1]
                    else:   
                        version=version_group[3]
            else:
                version=regex_results[int(version_group[1])-1]
      
            version=str(version)+str(version_group[0])
            version=re.sub("[^0-9\.]","",str(version))
            
    if not version:
        version="false"
    return version  
    




# Detecting Dom is not solved yet
def detectDom(data, driver, index, app):
    if driver.execute_script(str(data[app]["dom"])):
        result = {"detect":["dom"], "version":"False", "request":[], "response":[index], "url":[]}
        return result