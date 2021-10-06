import json
import os
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

default_allow_cat={12,18,27,22}
#default_allow_cat={12,18,27,22,28}
default_check_cat={12,18,27,22}
#default_check_cat={12,18,27,22,28}
json_path="./wappalyzer/"
categories_path="./wappalyzer/categories.json"
sig_url=list()

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


def extractJson(check_cat={12,18,27,22},allow_cat={12,18,27,22}):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    check_cat = set(check_cat)
    json_list = os.listdir(json_path)
    json_list.remove("categories.json")
    result={}
    for line in json_list:
        with open(json_path+line,encoding='UTF8') as json_file:
            json_data = json.load(json_file)
            for name in json_data:
                if set(check_cat) & set(json_data[name]['cats']):
                    if "headers" in json_data[name].keys():
                        for headers_key  in list(json_data[name]["headers"].keys()):
                            json_data[name]["headers"][headers_key.lower()] = json_data[name]["headers"].pop(headers_key)
                    result[name]=json_data[name]
    return result

def extractJsonattribute(result):
    attr=set()
    for name in result:
        attr.update(result[name].keys())
    return list(attr) 

def rebuildPattern(pattern):
    version_group="false"
    confidence="false"
    result = pattern.split('\\;')
    if len(result) > 1:
        for result_line in result[1:]:
            if "version:" in result_line:
                version_group=result_line.split(":\\")[1]
                version_group=int(version_group)
            if "confidence:" in result_line:
                confidence=result_line.split(":")[1]
                confidence=int(confidence)
    return result[0],version_group,confidence

def retVersiongroup(regex_results,version_group):
    if version_group == "false":
        return "false"
    else:
        for regex_result in regex_results:
            if version_group > 1:
                if(regex_result[version_group-1]):
                    return regex_result[version_group-1]
            else:
                if(regex_result):
                    return regex_result
    return "false"



def initResult(result,name):
    result[name]={}
    result[name]["detect"]=list()
    result[name]["version"]="false"
    result[name]["request"]=list()
    result[name]["response"]=list()

# requset_index , reseponse_index 가 0 이면 관련있는 index가 없다는 걸 의미
def appendResult(result,name,detectype,version,request_index=0,response_index=0):
    if name not in result:
        initResult(result,name)
    if detectype not in result[name]["detect"]:
        result[name]["detect"].append(detectype)
    if version != "false" and result[name]["version"] == "false":
        result[name]["version"]=version
    if request_index and request_index not in result[name]["request"]:
        result[name]["request"].append(request_index)
    if response_index and response_index not in result[name]["response"]:
        result[name]["response"].append(response_index)


def resBackend(driver,req_res_packets):
    target_url=driver.current_url
    current_page=driver.page_source
    soup = BeautifulSoup(current_page,"html.parser")
    result={}
    signature=extractJson(default_check_cat,default_allow_cat)
    for i,request in enumerate(req_res_packets):
        for  name  in signature:
            #url로 추출 
            if  'url' in  signature[name].keys():
                pattern,version_group,confidence=rebuildPattern(signature[name]["url"])
                regex_results=re.findall(pattern,request["request"]["full_url"],re.I)
                if(regex_results):
                    appendResult(result,name,"url",retVersiongroup(regex_results,version_group),i,0)
            #scripts src 현재 페이지에서 추출        
            if "scripts" in signature[name].keys():
                current_scripts = soup.select('script[src]') 
                if signature[name]["scripts"] is str:
                    pattern,version_group,confidence=rebuildPattern(signature[name]["scripts"])
                    for current_scripts_line in current_scripts:
                        regex_results=re.findall(pattern,current_scripts_line["src"],re.I)
                        if(regex_results):
                            appendResult(result,name,"scripts",retVersiongroup(regex_results,version_group),i,0)
                elif signature[name]["scripts"] is list:
                    for scripts_line in signature[name]["scripts"]:
                        pattern,version_group,confidence=rebuildPattern(scripts_line)
                        for current_scripts_line in current_scripts:
                            regex_results=re.findall(pattern,current_scripts_line["src"],re.I)
                            if(regex_results):
                                 appendResult(result,name,"scripts",retVersiongroup(regex_results,version_group),i,0)
            #header로 추출
            if  'headers' in  signature[name].keys():
                if not isSameDomain(target_url,request["request"]["full_url"]):
                    continue
                for comp_header in set(signature[name]["headers"].keys()) & set(request["request"]["headers"].keys()):
                    pattern,version_group,confidence=rebuildPattern(signature[name]["headers"][comp_header])
                    regex_results=re.findall(pattern,request["request"]["headers"][comp_header],re.I)
                    if(regex_results):
                        appendResult(result,name,"headers",retVersiongroup(regex_results,version_group),i,0)
                for comp_header in set(signature[name]["headers"].keys()) & set(request["response"]["headers"].keys()):
                    pattern,version_group,confidence=rebuildPattern(signature[name]["headers"][comp_header])
                    regex_results=re.findall(pattern,request["response"]["headers"][comp_header],re.I)
                    if(regex_results):
                        appendResult(result,name,"headers",retVersiongroup(regex_results,version_group),0,i)
            #cookie로 추출
            if  'cookie' in  signature[name].keys():
                if not isSameDomain(target_url,request["request"]["full_url"]):
                    continue
                #request packet 비교
                if "cookie" in signature[name]["headers"].keys():
                    pattern,version_group,confidence=rebuildPattern(signature[name]["headers"]["cookie"])
                    regex_results=re.findall(pattern,request["request"]["headers"]["cookie"],re.I)
                    if(regex_results):
                        appendResult(result,name,"cookie",retVersiongroup(regex_results,version_group),i,0)
                #response packet 비교
                for comp_cookie in ({"cookie","set-cookie"}  & set(signature[name]["headers"].keys())):
                        pattern,version_group,confidence=rebuildPattern(signature[name]["headers"]["cookie"])
                        regex_results=re.findall(pattern,request["response"]["headers"][comp_header],re.I)
                        if(regex_results):
                            appendResult(result,name,"cookie",retVersiongroup(regex_results,version_group),0,i)
            #html 파싱은 현재 페이질 경우만
            if 'html' in signature[name].keys():
                #str 일 경우
                if signature[name]["html"] is str:
                    pattern,version_group,confidence=rebuildPattern(signature[name]["html"])
                    regex_results=re.findall(pattern,current_page,re.I)
                    #현재 페이지는 response에서도 가져오기 때문에 response 패킷에 입력
                    if(regex_results):
                        appendResult(result,name,"html",retVersiongroup(regex_results,version_group),0,1)
                #list일 경우
                elif signature[name]["html"] is list:
                    for html_line in signature[name]["html"]:
                        pattern,version_group,confidence=rebuildPattern(html_line)
                        regex_results=re.findall(pattern,current_page,re.I)
                        #현재 페이지는 response에서도 가져오기 때문에 response 패킷에 입력
                        if(regex_results):
                            appendResult(result,name,"html",retVersiongroup(regex_results,version_group),0,1)
            #meta로 추출 , meta의 값은 dictionary 값 여러개도 가능
            if "meta" in signature[name].keys():
                metas = soup.select('meta[name][content]')
                for meta_line in metas:             
                    for comp_metakey in signature[name]["meta"]:
                        if meta_line['name'] == comp_metakey:
                            continue
                        pattern,version_group,confidence=rebuildPattern(signature[name]["meta"][comp_metakey])
                        regex_results=re.findall(pattern,meta_line["content"],re.I)
                        #현재 페이지는 response 패킷 1으로 침 
                        if(regex_results):
                            appendResult(result,name,"meta",retVersiongroup(regex_results,version_group),0,1)
    return(result)
                   

def extractPriority(cat=[12,18,27,22]):
    cat = sorted(cat)
    cat_priority={}
    print("extractprirority")
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        print(cat)
        for eachcat in cat:
            cat_priority[eachcat] = json_data[str(eachcat)]['priority']
    return cat_priority

#cat priority가 클수록 ,  같을 경우  카테고리가 번호가 우선 순위가 높다가정해서 선택 
def retCatrepresnt(check_cat,allow_cat):
    if len(check_cat) == 1:
        return check_cat
    else:
        cat_priority=extractPriority(check_cat)
        #cat_represent 우선 순위로 정해진 대표 cat 번호
        cat_reprent = -1
        while not cat_reprent in allow_cat:
            cat_reprent=max(cat_priority,key=cat_priority.get)
            del[cat_priority[cat_reprent]]
        #카테고리(cat) 번호 반환
        return cat_reprent

# retCatname(1) => cat 1 에 해당하는 이름 반환
def retCatname(singlecat):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        return json_data[str(singlecat)]#['name']

#retCatsname([12,13])으로 호출 가능 , name 반환   
def retCatsname(cat):
    #12(javascript framework),18(Web frameworks),22(web server),27(Programming Language)
    cat_name={}
    with open(categories_path,encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        for eachcat in cat:
            cat_name[str(eachcat)] = json_data[str(eachcat)]['name']
    return cat_name

if __name__ == '__main__':
    json_path="../wappalyzer/"
    categories_path="../wappalyzer/categories.json"
    print(extractJsonattribute(extractJson()))
    #print(retCatsname([12,18,27,22]))
    #print(18,retCatname(18))
    #resBackend()