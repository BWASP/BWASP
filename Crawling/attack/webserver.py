import json
import re
from urllib.parse import urlparse

category = [22, 28, 33, 34, 46]

def getWebServerInfo(target_url, req_res_packets, options):
    return_data = {}
    data = loadCategory(category)
    
    option_data = []
    for option in options:
        option_data.append(option["name"])

    for index, packet in enumerate(req_res_packets):
        if not isSameDomain(target_url, packet["request"]["full_url"]):
            continue
        
        ### 사용자가 지정한 서버 정보는 탐색하지 않음.
        webserver_keyword = list(data.keys())
        for d in webserver_keyword:
            if d.lower() in option_data:
                webserver_keyword.remove(d)
        ### End

        # check response Header
        for key in webserver_keyword:
            if not "headers" in list(data[key].keys()):
                continue
            
            for header in list(data[key]["headers"].keys()):
                if not header.lower() in list(packet["response"]["headers"].keys()):
                    continue

                regex = data[key]["headers"][header]
                regex = regex.replace("\\;version:\\1", "")
                
                # Find Server Info
                server_pattern = re.compile(regex)
                server_info = server_pattern.search(packet["response"]["headers"][header.lower()])
                if server_info != None:
                    if not key in list(return_data.keys()):
                        return_data[key] = {
                            "detect" : [],
                            "version" : "false",
                            "request" : [],
                            "response" : []
                        }

                    if not header in return_data[key]["detect"]:
                        return_data[key]["detect"].append(header)

                    return_data[key]["response"].append(index)

                    # Find Server Version Info
                    version_pattern = re.compile('([\d.]+)')
                    version_info = version_pattern.search(server_info.group())
                    if version_info != None:
                        return_data[key]["version"] = version_info.group()
    
    ### 사용자가 입력한 옵션 데이터를 수동으로 넣어줌
    for option in options:
        return_data[option["name"]] = {
            "detect" : [],
            "version" : option["version"],
            "request" : [],
            "response" : []
        }

    return return_data

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

if __name__ == "__main__":
    f = open("../test.json", "r", encoding="utf-8")
    data = json.load(f)
    f.close()

    result = getWebServerInfo("https://www.boannews.com/", data)
    print(json.dumps(result, indent=4))