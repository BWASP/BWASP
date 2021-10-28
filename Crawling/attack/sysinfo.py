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
    data = loadCategory(category)
    global cat_meta
    cat_meta=loadCategory_meta()
    detect_list = {}

    for i, packet in enumerate(req_res_packets):
        for app in data:
            cats = data[app]['cats']
            for option in options:
                if option['name'] == app:
                    appendResult(detect_list,cats,app,"option",option['version'],request_index=0,response_index=0)
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
    
    for option in options:
        detect_list[option['name']] = {
            "detect" : [],
            "version" : option['version'],
            "request" : [],
            "response" : [],
            "url" : []
        }

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



def initResult(detect_list,cats,name):  
    if cats not in detect_list.keys():
        detect_list[cats]=dict()
    
    if name not in detect_list[cats].keys():
        detect_list[cats][name]=dict()
        detect_list[cats][name]["detect"]=list()
        detect_list[cats][name]["version"]="false"
        detect_list[cats][name]["request"]=list()
        detect_list[cats][name]["response"]=list()
        detect_list[cats][name]["url"]=list()


# requset_index , reseponse_index 가 0 이면 관련있는 index가 없다는 걸 의미
def appendResult(detect_list,cats,name,detectype,version,request_index=0,response_index=0,url=""):

    cats = retCatrepresnt(cats) 
    initResult(detect_list,cats,name)
    if detectype and detectype not in detect_list[cats][name]["detect"]:
        detect_list[cats][name]["detect"].append(detectype)
    if version != "false" and detect_list[cats][name]["version"] == "false":
        detect_list[cats][name]["version"]=version
    if request_index and request_index not in detect_list[cats][name]["request"]:
        detect_list[cats][name]["request"].append(request_index)
    if response_index and response_index not in detect_list[cats][name]["response"]:
        detect_list[cats][name]["response"].append(response_index)
    if url and url not in detect_list[cats][name]["url"]:
        detect_list[cats][name]["url"].append(url)



# check response Header
def detectHeaders(detect_list,packet, data, index, cats, app):
    for header in list(data[app]["headers"].keys()):
        if not header.lower() in list(packet["response"]["headers"].keys()):
            continue

        regex = data[app]["headers"][header]
        pattern = re.compile(regex.split("\\;")[0])
        regex_result = pattern.search(packet["response"]["headers"][header.lower()])

        if regex_result:
            version = detectVersion(regex, packet["response"]["headers"][header.lower()])
            appendResult(detect_list,cats,app,"headers",version,0,index)

def detectHtml(detect_list, packet, data, index, cats, app):
    if type(data[app]["html"]) == str:
        pattern = re.compile(data[app]["html"].split("\\;")[0])
        regex_result = pattern.search(packet["response"]["body"])
        if regex_result:
            version = detectVersion(data[app]["html"], regex_result.group())
            appendResult(detect_list,cats,app,"html",version,0,index)
    else:
        for regex in data[app]["html"]:
            pattern = re.compile(regex.split("\\;")[0])
            regex_result = pattern.search(packet["response"]["body"])
            if regex_result:
                version = detectVersion(regex, regex_result.group())
                appendResult(detect_list,cats,app,"html",version,0,index)
                
    
    

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
            #result = {"detect":["cookies"], "version":"False", "request":[index], "response":[], "url":[]}

def detectUrl(detect_list, cur_page_links, data, cats, app):
    #version false 이유
    version ="false"
    for url in cur_page_links:
        if type(data[app]["url"]) == str:
            pattern = re.compile(data[app]["url"].split('\\;')[0])
            regex_result = pattern.search(url)
            
            if regex_result:
                version = detectVersion(data[app]["url"], url)
                appendResult(detect_list,cats,app,"url",version,0,1,url)
                return
        else:
            for url_regex in data[app]["url"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)

                if regex_result:
                    version = detectVersion(url_regex, url)
                    appendResult(detect_list,cats,app,"url",version,0,1,url)
                    return
    

def detectScripts(detect_list, cur_page_links, data, cats, app):
    for url in cur_page_links:
        if type(data[app]["scripts"]) == str:
            pattern = re.compile(data[app]["scripts"].split('\\;')[0])
            regex_result = pattern.search(url)
            if regex_result:
                version = detectVersion(data[app]["scripts"], url)
                appendResult(detect_list,cats,app,"scripts",version,0,1,url)
                return
        else:
            for url_regex in data[app]["scripts"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)
                if regex_result:
                    version = detectVersion(url_regex, url)
                    appendResult(detect_list,cats,app,"scripts",version,0,1,url)
                    return
    

def detectWebsite(detect_list, cur_page_links, data, cats, app):
    version="false"
     #version 비어 있는 문제
    for url in cur_page_links:
        if type(data[app]["website"]) == str:
            if data[app]["website"] in url:
                #1 => 현재 페이지
                appendResult(detect_list,cats,app,"website",version,0,1,url)
                return
        else:
            for url_cond in data[app]["website"]:
                if url_cond in url:
                     #1 => 현재 페이지
                    appendResult(detect_list,cats,app,"website",version,0,1,url)
                    return

def detectMeta(detect_list, packet, data, index, cats, app):
    version="false"
    html = BeautifulSoup(packet["response"]["body"], features="html.parser")
    for meta_regex in data[app]["meta"].values():
        print(meta_regex)
        try:
            pattern = re.compile(meta_regex.split('\\;')[0])
        except: 
            pattern = "vmkwdlwkw"
        meta_tag = html.find("meta", {"name":data[app]["meta"].keys()})
        if meta_tag and meta_tag.has_attr("content"):
            regex_result = pattern.search(meta_tag['content'])
            if regex_result:
                version = detectVersion(meta_regex, str(meta_tag))
                appendResult(detect_list,cats,app,"meta",version,0,index)

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
                        pattern = comp_metakey.split('\\;')[0]
                        regex_results=re.findall(pattern,meta_line["content"],re.I)
                        #현재 페이지는 response 패킷 1으로 침 
                        if(regex_results):
                            version = detectVersion(comp_metakey, meta_line["content"])
                            appendResult(detect_list,cats,app,"meta",version,0,index)
                    else:
                        pattern = data[app]["meta"][comp_metakey].split('\\;')[0]
                        regex_results=re.findall(pattern,meta_line["content"],re.I)
                    #현재 페이지는 response 패킷 1으로 침 
                    if(regex_results):
                        version = detectVersion(data[app]["meta"][comp_metakey], meta_line["content"])
                        appendResult(detect_list,cats,app,"meta",version,0,index)
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
    

# Detecting Dom is not solved yet
def detectDom(data, driver, index, app):
    if driver.execute_script(str(data[app]["dom"])):
        result = {"detect":["dom"], "version":"False", "request":[], "response":[index], "url":[]}
        return result