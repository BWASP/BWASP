import json
from urllib.parse import urlparse

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

def getCookies(url, req_res_packets):
    cookies_per_packet = dict()
    
    for packet in req_res_packets:
        cookies = dict()
        if not isSameDomain(url, packet["request"]["full_url"]) or "cookie" not in list(packet["request"]["headers"].keys()):
            continue

        for i in packet["request"]["headers"]["cookie"].split('; '):
            cookies[i.split('=')[0]] = i.split('=')[1]

        cookies_per_packet[packet["request"]["full_url"]] = cookies
    
    return cookies_per_packet

if __name__ == "__main__":
    req_res_packets = json.loads(open('./test.json','r').read())
    print(getCookies('https://kitribob.kr/', req_res_packets))