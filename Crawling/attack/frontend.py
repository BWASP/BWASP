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
def detectWebServer(url, cur_page_links, req_res_packets, driver, options):
    category = [12, 31, 59, 22, 44, 1]
    data = loadCategory(category)

    detect_list = dict()

    for i, packet in enumerate(req_res_packets):
        for app in data:
            for option in options:
                if option['name'] == app:
                    continue
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
    
    for option in options:
        detect_list[option['name']] = {
            "detect" : [],
            "version" : option['version'],
            "request" : [],
            "response" : [],
            "url" : []
        }

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
    result = None

    for header in list(data[app]["headers"].keys()):
        if not header.lower() in list(packet["response"]["headers"].keys()):
            continue

        regex = data[app]["headers"][header]
        pattern = re.compile(regex.split("\\;")[0])
        regex_result = pattern.search(packet["response"]["headers"][header.lower()])

        if regex_result != None:
            version = detectVersion(regex, packet["response"]["headers"][header.lower()])
            result = {"detect":["headers"], "version":version, "request":[], "response":[index], "url":[]}
            return result

def detectHtml(packet, data, index, app):
    result = None
    if type(data[app]["html"]) == str:
        pattern = re.compile(data[app]["html"].split("\\;")[0])
        regex_result = pattern.search(packet["response"]["body"])
        if regex_result != None:
            version = detectVersion(data[app]["html"], regex_result.group())
            result = {"detect":["html"], "version":version, "request":[], "response":[index], "url":[]}
    else:
        for regex in data[app]["html"]:
            pattern = re.compile(regex.split("\\;")[0])
            regex_result = pattern.search(packet["response"]["body"])
            if regex_result != None:
                version = detectVersion(regex, regex_result.group())
                if result is not None:
                    if version != 'False':
                        result['version'] = version
                else:
                    result = {"detect":["html"], "version":version, "request":[], "response":[index], "url":[]}
                
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
    result = None
    isExit = False
    for url in cur_page_links:
        if type(data[app]["url"]) == str:
            pattern = re.compile(data[app]["url"].split('\\;')[0])
            regex_result = pattern.search(url)
            
            if regex_result != None:
                version = detectVersion(data[app]["url"], url)
                result = {"detect":["url"], "version":version, "request":[], "response":[], "url":[url]}
                isExit = True
        else:
            for url_regex in data[app]["url"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)

                if regex_result != None:
                    version = detectVersion(url_regex, url)
                    if result is not None:
                        if version != 'False':
                            result['version'] = version
                    else:
                        result = {"detect":["url"], "version":version, "request":[], "response":[], "url":[url]}
                        isExit = True
        if isExit:
            break
    return result

def detectScripts(cur_page_links, data, app):
    result = None
    isExit = False
    for url in cur_page_links:
        if type(data[app]["scripts"]) == str:
            pattern = re.compile(data[app]["scripts"].split('\\;')[0])
            regex_result = pattern.search(url)
            if regex_result is not None:
                version = detectVersion(data[app]["scripts"], url)
                result = {"detect":["scripts"], "version":version, "request":[], "response":[], "url":[url]}
                isExit = True
        else:
            for url_regex in data[app]["scripts"]:
                pattern = re.compile(url_regex.split('\\;')[0])
                regex_result = pattern.search(url)
                if regex_result is not None:
                    version = detectVersion(url_regex, url)
                    if result is not None:
                        if version != 'False':
                            result['version'] = version
                    else:
                        result = {"detect":["scripts"], "version":version, "request":[], "response":[], "url":[url]}
                        isExit = True
        if isExit:
            break
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
        pattern = re.compile(meta_regex.split('\\;')[0])
        meta_tag = html.find("meta", {"name":data[app]["meta"].keys()})
        if meta_tag is not None and meta_tag.has_attr("content"):
            regex_result = pattern.search(meta_tag['content'])
            if regex_result is not None:
                version = detectVersion(meta_regex, str(meta_tag))
                result = {"detect":["meta"], "version":version, "request":[], "response":[index], "url":[]}
                return result

def detectVersion(full_regex, detected_info):
    if "\\;version:\\" not in full_regex:
        return "False"
                
    version_pattern = re.compile('(\\d+(\\.)?)+')
    version_info = version_pattern.search(detected_info)
    
    if version_info != None:
        return version_info.group()
    else:
        print("version info is not found")
        return "False"
    

# Detecting Dom is not solved yet
def detectDom(data, driver, index, app):
    if driver.execute_script(str(data[app]["dom"])) is not None:
        result = {"detect":["dom"], "version":"False", "request":[], "response":[index], "url":[]}
        return result

if __name__ == "__main__":
    url = "https://github.com/"
    
    driver = webdriver.Chrome('./Crawling/config/chromedriver')
    driver.get(url)

    options = {
                "tool": {
                    "analysisLevel": "771",
                    "optionalJobs": [
                        "portScan",
                        "CSPEvaluate"
                    ]
                },
                "info": {
                    "server": [
                        {
                            "name": "apache",
                            "version": "22"
                        },
                        {
                            "name": "nginx",
                            "version": "44"
                        }
                    ],
                    "framework": [
                        {
                            "name": "react",
                            "version": "22"
                        },
                        {
                            "name": "angularjs",
                            "version": "44"
                        }
                    ],
                    "backend": [
                        {
                            "name": "flask",
                            "version": "22"
                        },
                        {
                            "name": "django",
                            "version": "44"
                        }
                    ]
                },
                "target": {
                    "url": "https://github.com/",
                    "path": [
                    "/apply, /login", "/admin"
                    ]
                }
            }
    
    print(
        detectWebServer( # 파라미터 4개 (url, cur_page_links, req_res_packets, driver)
            url=url, 
            cur_page_links=["https://www.naver.com/devbridgeAutocomplete-min.js","https://github.com/jquery-14.0.1/jquery-migrate", "https://edgecastcdn.net/"], 
            req_res_packets=json.loads(open('./test.json','r').read()), 
            driver=driver,
            options=options['info']['framework']
        )
    )