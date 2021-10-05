import json
import os
import re
from urllib.parse import urlparse   

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
    return pattern.split("\\;")[0]

def initResult(result,name):
    result[name]={}
    result[name]["detect"]=list()
    result[name]["version"]="false"
    result[name]["request"]=list()
    result[name]["response"]=list()

# requset_index , reseponse_index 가 0 이면 관련있는 index가 없다는 걸 의미
def appendResult(result,name,detectype,request_index=0,response_index=0):
    if name not in result:
        initResult(result,name)
    if detectype not in result[name]["detect"]:
        result[name]["detect"].append(detectype)
    if request_index not in result[name]["request"]:
        result[name]["request"].append(request_index)
    if response_index not in result[name]["response"]:
        result[name]["response"].append(response_index)


def resBackend(target_url,req_res_packets):
    result={}
    signature=extractJson(default_check_cat,default_allow_cat)
    for i,request in enumerate(req_res_packets):
        for  name  in signature:
            #url로 추출 
            if  'url' in  signature[name].keys():
                pattern=rebuildPattern(signature[name]["url"])
                if re.findall(pattern,request["request"]["full_url"]):
                    appendResult(result,name,"url",i,0)
            #scripts src 도 url 처럼 추출        
            if  'scripts' in  signature[name].keys():
                if signature[name]["scripts"] is str:
                    pattern=rebuildPattern(scripts_line)
                    if re.findall(pattern,request["request"]["full_url"]):
                        appendResult(result,name,"scripts",i,0)
                elif signature[name]["scripts"] is list:
                    for scripts_line in signature[name]["scripts"]:
                        pattern=rebuildPattern(scripts_line)
                        if re.findall(pattern,request["request"]["full_url"]):
                            appendResult(result,name,"scripts",i,0)

            #header로 추출
            if  'headers' in  signature[name].keys():
                if not isSameDomain(target_url,request["request"]["full_url"]):
                    continue
                for comp_header in set(signature[name]["headers"].keys()) & set(request["request"]["headers"].keys()):
                    pattern=rebuildPattern(signature[name]["headers"][comp_header])
                    if re.findall(pattern,request["request"]["headers"][comp_header]):
                        appendResult(result,name,"headers",i,0)
                for comp_header in set(signature[name]["headers"].keys()) & set(request["response"]["headers"].keys()):
                    pattern=rebuildPattern(signature[name]["headers"][comp_header])
                    if re.findall(pattern,request["response"]["headers"][comp_header]):
                        appendResult(result,name,"headers",0,i)
                
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