import json
import re
from urllib.parse import urlparse

category = [22]

def getWebServerInfo(target_url, req_res_packets):
    data = loadCategory(category)
    
    for packet in req_res_packets:
        if not isSameDomain(target_url, packet["request"]["full_url"]):
            continue
        
        # check response Header
        for key in data:
            if not "headers" in list(data[key].keys()):
                continue

            for header in list(data[key]["headers"].keys()):
                if not header.lower() in list(packet["response"]["headers"].keys()):
                    continue

                regex = data[key]["headers"][header]
                regex = regex.replace("\\;version:\\1", "")
                
                pattern = re.compile(regex)
                if pattern.search(packet["response"]["headers"][header.lower()]) != None:
                    print("Server: {}".format(key))
                    print("Packet: {}\n\n\n".format(json.dumps(packet["response"]["headers"], indent=4)))

def loadCategory(category):
    return_data = {}

    for name in "abcdefghijklmnopqrstuvwxyz_":
        file = "../wappalyzer/{}.json".format(name)

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
        target_domain = urlparse(target_url).netloc
        visit_domain = urlparse(visit_url).netloc
        
        if target_domain == visit_domain:
            return True
        else:
            return False
    except:
        return False

if __name__ == "__main__":
    f = open("../test.json", "r", encoding="utf-8")
    data = json.load(f)
    f.close()

    getWebServerInfo("https://www.casper.or.kr/", data)