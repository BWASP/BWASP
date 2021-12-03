# =========================== 나중에 다시 참고해야 할 것 ===============================
"""
start_options["previous_packet_count"] += len(req_res_packets)
recent_packet_count =  len(req_res_packets) + previous_packet_count
    # {"id": "[1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]"}
    if len(loadpacket_indexes) < recent_packet_count:
        #수정 후 loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"])["id"]
        loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"]["id"])

        packet_indexes = loadpacket_indexes[previous_packet_count:recent_packet_count]
    #analyst_result = analyst.start(sysinfo_detectlist,input_url, req_res_packets, cur_page_links, packet_indexes,options['info'])
    # res_req_packet index는 0 부터 시작하는데 ,  해당 index가 4인경우 realted packet에 packet_indexes[4]로 넣으면 됨

    loadpacket_indexes = list()  # automation packet indexes
"""

import re, json, sys, os

#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


from modules import db
from modules import get_cookies
from modules.attack_vector import *
from modules.api import *


def start(receive):
    loadpacket_indexes = list()  # automation packet indexes

    http_method = "None"
    infor_vector = "None"
    robots_result = False
    error_result = False

    """
    current_url = "https://webhacking.kr/"
    
    receive = {
      current_url: [{'request': {'method': 'GET', 'url': '/collect?v=1&_v=j96&a=1669515803&t=pageview&_s=1&dl=http%3A%2F%2Fsuninatas.com%2Fboard%2Fnotice&ul=ko-kr&de=UTF-8&dt=%EC%8D%A8%EB%8B%88%EB%82%98%ED%83%80%EC%8A%A4&sd=24-bit&sr=1536x864&vp=1019x718&je=0&_u=QACAAUAB~&jid=&gjid=&cid=963221336.1636827681&tid=UA-103021028-2&_gid=1241354806.1636827681&gtm=2ouba1&z=783593795', 'headers': {'host': 'www.google-analytics.com', 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"', 'sec-ch-ua-mobile': '?0', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36', 'sec-ch-ua-platform': '"Windows"', 'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'no-cors', 'sec-fetch-dest': 
    'image', 'referer': 'http://suninatas.com/', 'accept-encoding': 'gzip, deflate, br', 'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}, 'body': '', 'full_url': 'https://www.google-analytics.com/collect?v=1&_v=j96&a=1669515803&t=pageview&_s=1&dl=http%3A%2F%2Fsuninatas.com%2Fboard%2Fnotice&ul=ko-kr&de=UTF-8&dt=%EC%8D%A8%EB%8B%88%EB%82%98%ED%83%80%EC%8A%A4&sd=24-bit&sr=1536x864&vp=1019x718&je=0&_u=QACAAUAB~&jid=&gjid=&cid=963221336.1636827681&tid=UA-103021028-2&_gid=1241354806.1636827681&gtm=2ouba1&z=783593795'}, 'response': {'headers': {'access-control-allow-origin': '*', 'date': 'Sat, 13 Nov 2021 09:37:55 GMT', 'pragma': 'no-cache', 'expires': 'Mon, 01 Jan 1990 00:00:00 GMT', 'last-modified': 'Sun, 17 May 1998 03:00:00 GMT', 'x-content-type-options': 'nosniff', 'content-type': 'image/gif', 'cross-origin-resource-policy': 
    'cross-origin', 'server': 'Golfe2', 'content-length': '35', 'age': '31421', 'cache-control': 'no-cache, no-store, must-revalidate', 'alt-svc': 'clear'}, 'body': '', 'status_code': 200}}]
    }
    
    receive = {
        "https://webhacking.kr/": [{
            'request': {'method': 'GET', 'url': '/s/lato/v20/S6uyw4BMUTPHjx4wXg.woff2',
                        'headers': {'host': 'fonts.gstatic.com', 'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                                    'origin': 'https://webhacking.kr', 'sec-ch-ua-mobile': '?0',
                                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                                    'sec-ch-ua-platform': '"Windows"', 'accept': '*/*', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'font',
                                    'referer': 'https://fonts.googleapis.com/', 'accept-encoding': 'gzip, deflate, br',
                                    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}, 'body': '',
                        'full_url': 'https://fonts.gstatic.com/s/lato/v20/S6uyw4BMUTPHjx4wXg.woff2'
                        },
            'response': {
                'headers': {'accept-ranges': 'bytes', 'content-type': 'font/woff2', 'access-control-allow-origin': '*',
                            'content-security-policy-report-only': "require-trusted-types-for 'script'; report-uri https://csp.withgoogle.com/csp/apps-themes",
                            'cross-origin-resource-policy': 'cross-origin', 'cross-origin-opener-policy-report-only': 'same-origin; report-to="apps-themes"',
                            'report-to': '{"group":"apps-themes","max_age":2592000,"endpoints":[{"url":"https://csp.withgoogle.com/csp/report-to/apps-themes"}]}',
                            'timing-allow-origin': '*', 'content-length': '23484', 'date': 'Fri, 12 Nov 2021 09:12:07 GMT', 'expires': 'Sat, 12 Nov 2022 09:12:07 GMT',
                            'last-modified': 'Tue, 10 Aug 2021 00:19:01 GMT', 'x-content-type-options': 'nosniff', 'server': 'sffe', 'x-xss-protection': '0',
                            'cache-control': 'public, max-age=31536000', 'age': '123568', 'alt-svc': 'clear'}, 'body': '', 'status_code': 200
            }
        }]
    }
    """

    http_method, infor_vector = attackHeader(list(receive.keys())[0])
    robots_result = robotsTxt(list(receive.keys())[0])
    error_result = errorPage(list(receive.keys())[0])

    # req_res_packets = db.deleteUselessBody(receive[list(receive.keys())[0]][0])  # CRX 패킷을 deleteUselessBody 통과 되도록
    req_res_packets = receive[list(receive.keys())[0]]  # [0]  # CRX 패킷을 deleteUselessBody 통과 되도록
    cookie_result = get_cookies.start(list(receive.keys())[0], req_res_packets)

    #
    # req_res_packets = #자동쪽의 패킷 값 가져오게
    # cookie_result = #자동쪽의 쿠키 값 가져오게
    #
    
    

    previous_packet_count = Packets().GetManualCount()["retData"]["count"]
    db.insertPackets(req_res_packets)
    recent_packet_count =  len(req_res_packets) + previous_packet_count
    packet_indexes = json.loads(Packets().GetManualIndex()["retData"]["id"])[previous_packet_count:recent_packet_count]
    result = db.insertDomains(req_res_packets, cookie_result, packet_indexes, list(receive.keys())[0], http_method, infor_vector,
                              robots_result, error_result)

    return json.dumps(result)
