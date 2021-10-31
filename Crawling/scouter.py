from seleniumwire import webdriver
from multiprocessing import Process
from urllib.parse import urlparse, urlunparse
from webdriver_manager.chrome import ChromeDriverManager

from Crawling import analyst
from Crawling.feature import get_page_links, packet_capture, get_res_links, get_ports, get_cookies, get_domains, csp_evaluator, db, func
from Crawling.attack_vector import attack_header
import json
# TODO
# 사용자가 여러개의 사이트를 동시에 테스트 할 때, 전역 변수의 관리 문제
start_options = {
    "check" : True,
    "input_url" : "",
    "visited_links" : [],
    "count_links" : {},
    "previous_packet_count" : 0 #누적 패킷 개수
}

sysinfo_detectlist = {}
loadpacket_indexes = list() # automation packet indexes 

def start(url, depth, options):
    global start_options
    driver = initSelenium()
    visit(driver, url, depth, options)
    driver.quit()
    
    start_options["check"] = True
    start_options["input_url"] = ""
    start_options["visited_links"] = []
    start_options["count_links"] = {}

def analysis(input_url, req_res_packets, cur_page_links, options, cookie_result, page_source, current_url,previous_packet_count):
    global start_options
    global sysinfo_detectlist
    global loadpacket_indexes

    recent_packet_count =  len(req_res_packets) + len(previous_packet_count)
    # {"id": "[1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]"}     
    if len(loadpacket_indexes) < recent_packet_count:
        # rest api 개발되면 사용 loadpacket_indexes= json.loads(db.Packets.GetAutomationIndex()["id"])
        loadpacket_indexes = list(range(1,len(loadpacket_indexes)*2)) # rest api 전 호환을 위한 위의 임시 코드 
    
    packet_indexes = loadpacket_indexes[previous_packet_count:recent_packet_count]
    analyst_result = analyst.start(sysinfo_detectlist,input_url, req_res_packets, cur_page_links, packet_indexes,options['info'])
    # res_req_packet index는 0 부터 시작하는데 ,  해당 index가 4인경우 realted packet에 packet_indexes[4]로 넣으면 됨     
    db.insertDomains(req_res_packets, cookie_result,packet_indexes , current_url)
    db.insertWebInfo(analyst_result, input_url,packet_indexes)
    
    return 1

def visit(driver, url, depth, options):
    global start_options

    try:
        driver.get(url)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        pass

    if start_options["check"]:
        attack_header(driver.current_url)
        start_options["input_url"] = driver.current_url
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
    if not func.isSameDomain(driver.current_url, start_options["input_url"]):
        req_res_packets = packet_capture.filterDomain(req_res_packets, start_options["input_url"])
        cur_page_links = list()
    else:
        cur_page_links = get_page_links.start(driver.current_url, driver.page_source)
        cur_page_links += get_res_links.start(driver.current_url, req_res_packets, driver.page_source)
        cur_page_links = list(set(packet_capture.deleteFragment(cur_page_links)))
        # domain_result = get_domains.start(dict(), driver.current_url, cur_page_links)
    cookie_result = get_cookies.start(driver.current_url, req_res_packets)

    req_res_packets = packet_capture.deleteUselessBody(req_res_packets)
    db.insertPackets(req_res_packets)
    p = Process(target=analysis, args=(start_options['input_url'], req_res_packets, cur_page_links, options, cookie_result, driver.page_source, driver.current_url,start_options["previous_packet_count"])) # driver 전달 시 에러. (프로세스간 셀레니움 공유가 안되는듯 보임)
    start_options["previous_packet_count"] += len(req_res_packets)
    p.start()
    
    if depth == 0:
        return

    for visit_url in cur_page_links:
        if visit_url in start_options["visited_links"]:
            continue
        if not func.isSameDomain(start_options["input_url"], visit_url):
            continue
        if func.isSamePath(visit_url, start_options["visited_links"]):
            continue
        if func.isExistExtension(visit_url, "image"):
            continue
        if checkCountLink(visit_url, start_options["count_links"]):
            continue
        
        start_options["visited_links"].append(visit_url)
        visit(driver, visit_url, depth - 1, options)

def checkCountLink(visit_url, count_links):
    visit_path = urlparse(visit_url).path

    try:
        if count_links[visit_path]["count"] > 10:
            return True

        count_links[visit_path]["count"] += 1
    except:
        start_options["count_links"][visit_path] = {"count" : 1}

    return False

def initSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_experimental_option("prefs", {
        "download_restrictions": 3
    })
    options = {
        "disable_encoding": True
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
