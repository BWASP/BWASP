from seleniumwire import webdriver
from multiprocessing import Process, Manager , Lock
from urllib.parse import urlparse, urljoin
from webdriver_manager.chrome import ChromeDriverManager
import re,json

from Crawling import analyst
from Crawling.feature import get_page_links, packet_capture, get_res_links, get_ports, get_cookies, csp_evaluator, db, func
from Crawling.feature.api import *
from Crawling.attack_vector import attackHeader, robotsTxt

# TODO
# 사용자가 여러개의 사이트를 동시에 테스트 할 때, 전역 변수의 관리 문제
start_options = {
    "check" : True,
    "input_url" : "",
    "visited_links" : [],
    "count_links" : {},
    "previous_packet_count" : 0 #누적 패킷 개수
}

loadpacket_indexes = list() # automation packet indexes 
process_list = list()
http_method = "None"
infor_vector = "None"
robots_result = False

def start(url, depth, options):
    global start_options
    global process_list
    global detect_list
    global lock

    manager = Manager()
    detect_list = manager.list()
    detect_list.append({})
    lock = manager.Lock()
    driver = initSelenium()
    visit(driver, url, depth, options)
    for each_process in process_list:
        each_process.join()
    driver.quit()
    
    start_options["check"] = True
    start_options["input_url"] = ""
    start_options["visited_links"] = []
    start_options["count_links"] = {}

def analysis(input_url, req_res_packets, cur_page_links, options, cookie_result,detect_list,lock,current_url,previous_packet_count,http_method, infor_vector, robots_result):
    global start_options
    global loadpacket_indexes

    recent_packet_count =  len(req_res_packets) + previous_packet_count
    # {"id": "[1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]"}     
    if len(loadpacket_indexes) < recent_packet_count:
        #수정 후 loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"])["id"]
        loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"]["id"])

    packet_indexes = loadpacket_indexes[previous_packet_count:recent_packet_count]
    #analyst_result = analyst.start(sysinfo_detectlist,input_url, req_res_packets, cur_page_links, packet_indexes,options['info'])
    analyst.start(detect_list,lock, input_url, req_res_packets, cur_page_links, current_url, packet_indexes,options['info'])
    # res_req_packet index는 0 부터 시작하는데 ,  해당 index가 4인경우 realted packet에 packet_indexes[4]로 넣으면 됨     


    db.insertDomains(req_res_packets, cookie_result,packet_indexes , input_url, http_method, infor_vector, robots_result) #current_url을 input_url로 바꿈 openredirect 탐지를 위해 (11-07)_
    db.updateWebInfo(detect_list[0])
    
    return 1

def visit(driver, url, depth, options):
    global start_options
    global process_list
    global detect_list
    global lock
    global http_method
    global infor_vector
    global robots_result

    try:
        driver.get(url)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        pass

    if start_options["check"]:
        http_method, infor_vector = attackHeader(driver.current_url)
        robots_result = robotsTxt(driver.current_url)
        start_options["input_url"] = driver.current_url
        db.postWebInfo(start_options["input_url"])
        start_options["visited_links"].append(start_options["input_url"])

        start_options["check"] = False

        if "portScan" in options["tool"]["optionalJobs"]:
            target_port = get_ports.getPortsOffline(start_options["input_url"])
            db.insertPorts(target_port, start_options["input_url"])
        else:
            target_port = get_ports.getPortsOnline(start_options["input_url"])
            db.insertPorts(target_port, start_options["input_url"])

    if "CSPEvaluate" in options["tool"]["optionalJobs"]:
        csp_result = csp_evaluator.start(driver.current_url)
        db.insertCSP(csp_result)

    req_res_packets = packet_capture.start(driver)

    # 다른 사이트로 Redirect 되었는지 검증.
    if isOpenRedirection(url, driver.current_url, start_options["input_url"]):
        # print("Open Redirect Detect: {}".format(url))
        req_res_packets = packet_capture.filterPath(req_res_packets, url)
        req_res_packets[0]["open_redirect"] = True
        cur_page_links = list()
    else:
        cur_page_links = get_page_links.start(driver.current_url, driver.page_source)
        cur_page_links += get_res_links.start(driver.current_url, req_res_packets, driver.page_source)
        cur_page_links = list(set(packet_capture.deleteFragment(cur_page_links)))
    cookie_result = get_cookies.start(driver.current_url, req_res_packets)

    req_res_packets = packet_capture.deleteUselessBody(req_res_packets)
    db.insertPackets(req_res_packets)
    p = Process(target=analysis, args=(start_options['input_url'], req_res_packets, cur_page_links, options, cookie_result,detect_list,lock,driver.current_url,start_options["previous_packet_count"],http_method, infor_vector, robots_result)) # driver 전달 시 에러. (프로세스간 셀레니움 공유가 안되는듯 보임)
    start_options["previous_packet_count"] += len(req_res_packets)
    p.start()
    process_list.append(p)
    
    if depth == 0:
        return

    for visit_url in cur_page_links:
        if visit_url in start_options["visited_links"]:
            continue
        if not func.isSameDomain(start_options["input_url"], visit_url):
            continue
        if func.isSamePath(visit_url, start_options["visited_links"]):
            continue
        if func.isExistExtension(visit_url, ["image"]):
            continue
        if checkCountLink(visit_url, start_options["count_links"]):
            continue
        
        start_options["visited_links"].append(visit_url)
        visit(driver, visit_url, depth - 1, options)

def checkCountLink(visit_url, count_links):
    visit_path = urlparse(visit_url).path
    tmp_path = visit_path.split("/")

    for path in tmp_path[::-1]:
        if path.isnumeric():
            tmp_path.pop()

    visit_path = "/".join(tmp_path)

    try:
        if count_links[visit_path]["count"] > 5:
            return True

        count_links[visit_path]["count"] += 1
    except:
        start_options["count_links"][visit_path] = {"count" : 1}

    return False

'''
    String visit_url: 방문한 url
    String current_url: 현재 페이지의 url
    String target_url: 사용자가 입력한 url 
'''
def isOpenRedirection(visit_url, current_url, target_url):
    url = urlparse(visit_url)
    if url.query:
        url_query = url.query.split("&")

        if not func.isSameDomain(current_url, target_url) or not func.isSamePath(visit_url, current_url):
            pattern_url = re.compile("((?:http|ftp|https)(?:://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)")
            
            for query in url_query:
                value = query.split("=")
                if len(value) == 1:
                    continue
                
                value = value[1]
                if pattern_url.findall(value):
                    return True
                if urljoin(target_url, value) == current_url:
                    return True
            return False
    return False

def initSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_experimental_option("prefs", {
        "download_restrictions": 3
    })
    # https://github.com/wkeeling/selenium-wire#in-memory-storage
    options = {
        "disable_encoding": True,
        'request_storage': 'memory'
    }

    driver = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=options, chrome_options=chrome_options)

    return driver

if __name__ == "__main__":
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
            "url": "http://testphp.vulnweb.com/",
            "path": [
                "/apply, /login", "/admin"
            ]
        }
    }

    start(options["target"]["url"], int(options["tool"]["analysisLevel"]), options["info"])
