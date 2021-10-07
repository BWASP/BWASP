import json, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver

'''
"59": {
    "name": "JavaScript libraries",
    "priority": 9
},  
"31": {
    "name": "CDN",
    "priority": 9
}
"12": {
    "name": "JavaScript frameworks",
    "priority": 8
},

[
    'cats', 'description', 'html', 'icon', 'oss', 'website', 'xhr', 'js', 'scripts', 'cpe', 'headers', 
    'implies', 'url', 'cookies', 'pricing', 'saas', 'dns', 'dom', 'excludes', 'meta', 'requires'
]
    
scripts(O), headers(O), cookies(O), dom(O), meta(O), url(O), html(O), website(O)
'''

# Main Function
def detectWebServer(url, cur_page_links, req_res_packets, driver):
    category = [12, 31, 59]
    data = loadCategory(category)

    detect_list = dict()

    for i, packet in enumerate(req_res_packets):

        for app in data:
            # Including external domain as well as including same domain
            if not isSameDomain(url, packet["request"]["full_url"]):
                if "scripts" in list(data[app].keys()):
                    result = detectScripts(cur_page_links, data, app)
                    detect_list = resultFunc(detect_list, app, result)
                if "website" in list(data[app].keys()):
                    result = detectWebsite(cur_page_links, data, app)
                    detect_list = resultFunc(detect_list, app, result)
            else:
                if "url" in list(data[app].keys()):
                    result = detectUrl(cur_page_links, data, app)
                    detect_list = resultFunc(detect_list, app, result)
                if "headers" in list(data[app].keys()):
                    result = detectHeaders(packet, data, i, app)
                    detect_list = resultFunc(detect_list, app, result)
                if "html" in list(data[app].keys()):
                    result = detectHtml(packet, data, i, app)
                    detect_list = resultFunc(detect_list, app, result)
                if "cookies" in list(data[app].keys()):
                    result = detectCookies(packet, data, i, app)
                    detect_list = resultFunc(detect_list, app, result)
                if "meta" in list(data[app].keys()):
                    result = detectMeta(packet, data, i, app)
                    detect_list = resultFunc(detect_list, app, result)
                # if "dom" in list(data[app].keys()):
                #     result = detectDom(data, driver, i, app)
                #     detect_list = resultFunc(detect_list, app, result)
    
    return detect_list


def loadCategory(category):
    return_data = {}

    for name in "abcdefghijklmnopqrstuvwxyz_":
        file = "./wappalyzer/{}.json".format(name)

        f = open(file, "r", encoding="utf-8")
        data = json.load(f)
        f.close()

        for key in data.keys():
            for cat in category:
                if cat in data[key]["cats"]:
                    return_data[key] = data[key]
                    
    return return_data

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

def resultFunc(detect_list, app, result):
    if result is not None:
        if app in detect_list.keys():
            for key in ["detect","request","response","url"]:
                for items in result[key]:
                    if items not in detect_list[app][key]:
                        detect_list[app][key].append(items)
            if result["version"] != "False":
                detect_list[app]["version"] = result["version"]
        else:
            detect_list[app] = result

    return detect_list

# check response Header
def detectHeaders(packet, data, index, app):
    for header in list(data[app]["headers"].keys()):
        if not header.lower() in list(packet["response"]["headers"].keys()):
            continue

        regex = data[app]["headers"][header]
        regex = regex.split("\\;version:\\")[0]
        pattern = re.compile(regex)

        if pattern.search(packet["response"]["headers"][header.lower()]) != None:
            result = {"detect":["headers"], "version":"False", "request":[], "response":[index], "url":[]}
            return result

def detectHtml(packet, data, index, app):
        if type(data[app]["html"]) == str:
            pattern = re.compile(data[app]["html"].split("\\;version:\\")[0])
            if pattern.search(packet["response"]["body"]) != None:
                result = {"detect":["html"], "version":"False", "request":[], "response":[index], "url":[]}
                return result
        else:
            for regex in data[app]["html"]:
                pattern = re.compile(regex.split("\\;version:\\")[0])

                if pattern.search(packet["response"]["body"]) != None:
                    result = {"detect":["html"], "version":"False", "request":[], "response":[index], "url":[]}
                    return result

def detectCookies(packet, data, index, app):
    cookies = dict()
    if "cookie" not in list(packet["request"]["headers"].keys()):
        return None
    for i in packet["request"]["headers"]["cookie"].split('; '):
        cookies[i.split('=')[0]] = i.split('=')[1]
    for cookie in data[app]["cookies"]:
        if cookie in cookies.keys():
            result = {"detect":["cookies"], "version":"False", "request":[index], "response":[], "url":[]}
            return result

def detectUrl(cur_page_links, data, app):
    for url in cur_page_links:
        if type(data[app]["url"]) == str:
            pattern = re.compile(data[app]["url"])
            if pattern.search(url) != None:
                result = {"detect":["url"], "version":"False", "request":[], "response":[], "url":[url]}
                return result
        else:
            for url_regex in data[app]["url"]:
                pattern = re.compile(url_regex)
                if pattern.search(url) != None:
                    result = {"detect":["url"], "version":"False", "request":[], "response":[], "url":[url]}
                    return result

def detectScripts(cur_page_links, data, app):
    for url in cur_page_links:
        if type(data[app]["scripts"]) == str:
            pattern = re.compile(data[app]["scripts"])
            if pattern.search(url) != None:
                result = {"detect":["scripts"], "version":"False", "request":[], "response":[], "url":[url]}
                return result
        else:
            for url_regex in data[app]["scripts"]:
                pattern = re.compile(url_regex)
                if pattern.search(url) != None:
                    result = {"detect":["scripts"], "version":"False", "request":[], "response":[], "url":[url]}
                    return result

def detectWebsite(cur_page_links, data, app):
    for url in cur_page_links:
        if type(data[app]["website"]) == str:
            if data[app]["website"] in url:
                result = {"detect":["website"], "version":"False", "request":[], "response":[], "url":[url]}
                return result
        else:
            for url_cond in data[app]["website"]:
                if url_cond in url:
                    result = {"detect":["website"], "version":"False", "request":[], "response":[], "url":[url]}
                    return result

def detectMeta(packet, data, index, app):
    html = BeautifulSoup(packet["response"]["body"], features="html.parser")
    for meta_regex in data[app]["meta"].values():
        pattern = re.compile(meta_regex)
        meta_tag = html.find("meta", {"name":data[app]["meta"].keys()})
        if meta_tag is not None and meta_tag.has_attr("content"):
            if pattern.search(meta_tag['content']) is not None:
                result = {"detect":["meta"], "version":"False", "request":[], "response":[index], "url":[]}
                return result

# Detecting Dom is not solved yet
def detectDom(data, driver, index, app):
    if driver.execute_script(str(data[app]["dom"])) is not None:
        result = {"detect":["dom"], "version":"False", "request":[], "response":[index], "url":[]}
        return result

if __name__ == "__main__":
    url = "https://www.cloudflare.com/"
    
    driver = webdriver.Chrome('./Crawling/config/chromedriver')
    driver.get(url)

    req_res_packets = json.loads(open('./test.json','r').read())
    
    print(
        detectWebServer( # 파라미터 4개 (url, cur_page_links, req_res_packets, driver)
            url=url, 
            cur_page_links=["https://www.naver.com/devbridgeAutocomplete-min.js","https://github.com/jquery/jquery-migrate", "https://edgecastcdn.net/"], 
            req_res_packets=json.loads(open('./test.json','r').read()), 
            driver=driver
        )
    )