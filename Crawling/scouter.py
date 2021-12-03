from seleniumwire import webdriver
from multiprocessing import Process, Manager
from urllib.parse import urlparse, urljoin
from webdriver_manager.chrome import ChromeDriverManager
import re, json

from Crawling import analyst
from Crawling.feature.packet_capture import PacketCapture
from Crawling.feature.get_res_links import GetReslinks
from Crawling.feature.csp_evaluator import cspAnalysis
from Crawling.feature.get_ports import GetPort
from Crawling.feature.get_page_links import GetPageLinks
from Crawling.feature import get_cookies, db, func
from Crawling.feature.api import *
from Crawling.attack_vector import attackHeader, robotsTxt, errorPage, directoryIndexing, adminPage


def initGlobal():
    global START_OPTIONS
    global ANALYSIS_DATA
    global LOAD_PACKET_INDEXES
    global PROCESS_LIST
    global DETECT_LIST
    global LOCK

    START_OPTIONS = {
        "check": True,
        "input_url": "",
        "visited_links": [],
        "count_links": {},
        "previous_packet_count": 0  # 누적 패킷 개수
    }

    ANALYSIS_DATA = {
        "http_method": None,
        "infor_vector": None,
        "robots_result": False,
        "error_result": False,
        "directory_indexing": list(),
        "admin_page": list()
    }

    LOAD_PACKET_INDEXES = list()  # automation packet indexes
    PROCESS_LIST = list()
    DETECT_LIST = list()
    LOCK = None


initGlobal()


def start(url, depth, options):
    global START_OPTIONS
    global PROCESS_LIST
    global DETECT_LIST
    global LOCK

    manager = Manager()
    DETECT_LIST = manager.list()
    DETECT_LIST.append({})
    LOCK = manager.Lock()

    driver = initSelenium()
    visit(driver, url, depth, options)

    for each_process in PROCESS_LIST:
        each_process.join()

    driver.quit()
    initGlobal()


def analysis(input_url, req_res_packets, cur_page_links, options, cookie_result, DETECT_LIST, LOCK, current_url, previous_packet_count, ANALYSIS_DATA):
    global START_OPTIONS
    global LOAD_PACKET_INDEXES

    recent_packet_count = len(req_res_packets) + previous_packet_count
    # {"id": "[1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]"}     
    if len(LOAD_PACKET_INDEXES) < recent_packet_count:
        # 수정 후 LOAD_PACKET_INDEXES = json.loads(Packets().GetAutomationIndex()["retData"])["id"]
        LOAD_PACKET_INDEXES = json.loads(Packets().GetAutomationIndex()["retData"]["id"])

    packet_indexes = LOAD_PACKET_INDEXES[previous_packet_count: recent_packet_count]
    # analyst_result = analyst.start(sysinfo_detectlist,input_url, req_res_packets, cur_page_links, packet_indexes,options['info'])
    analyst.start(DETECT_LIST, LOCK, input_url, req_res_packets, cur_page_links, current_url, packet_indexes, options['info'])
    # res_req_packet index는 0 부터 시작하는데 ,  해당 index가 4인경우 realted packet에 packet_indexes[4]로 넣으면 됨     

    db.insertDomains(req_res_packets, cookie_result, packet_indexes, input_url, ANALYSIS_DATA)  # current_url을 input_url로 바꿈 openredirect 탐지를 위해 (11-07)_
    db.updateWebInfo(DETECT_LIST[0])

    return 1


def visit(driver, url, depth, options):
    global START_OPTIONS
    global ANALYSIS_DATA
    global PROCESS_LIST
    global DETECT_LIST
    global LOCK

    try:
        driver.get(url)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        pass

    if START_OPTIONS["check"]:
        ANALYSIS_DATA["directory_indexing"] = directoryIndexing(driver.current_url)
        ANALYSIS_DATA["admin_page"] = adminPage(driver.current_url)
        ANALYSIS_DATA["http_method"], ANALYSIS_DATA["infor_vector"] = attackHeader(driver.current_url)
        ANALYSIS_DATA["robots_result"] = robotsTxt(driver.current_url)
        ANALYSIS_DATA["error_result"] = errorPage(driver.current_url)
        db.postWebInfo(driver.current_url)

        START_OPTIONS["input_url"] = driver.current_url
        START_OPTIONS["visited_links"].append(START_OPTIONS["input_url"])
        START_OPTIONS["check"] = False

        if "portScan" in options["tool"]["optionalJobs"]:
            target_port = GetPort().getPortsOffline(START_OPTIONS["input_url"])
            db.insertPorts(target_port, START_OPTIONS["input_url"])
        else:
            target_port = GetPort().getPortsOnline(START_OPTIONS["input_url"])
            db.insertPorts(target_port, START_OPTIONS["input_url"])

        if "CSPEvaluate" in options["tool"]["optionalJobs"]:
            csp_result = cspAnalysis().start(driver.current_url)
            db.insertCSP(csp_result)

    packet_obj = PacketCapture()
    packet_obj.start(driver)

    # 다른 사이트로 Redirect 되었는지 검증.
    if isOpenRedirection(url, driver.current_url, START_OPTIONS["input_url"]):
        packet_obj.filterPath(url)
        packet_obj.packets[0]["open_redirect"] = True
        cur_page_links = list()
    else:
        cur_page_links = GetPageLinks(driver.current_url, driver.page_source).start()
        cur_page_links += GetReslinks(driver.current_url, packet_obj.packets, driver.page_source).start()
        cur_page_links = list(set(packet_obj.deleteFragment(cur_page_links)))
    cookie_result = get_cookies.start(driver.current_url, packet_obj.packets)

    packet_obj.deleteUselessBody()
    db.insertPackets(packet_obj.packets)
    p = Process(target=analysis, args=(
    START_OPTIONS['input_url'], packet_obj.packets, cur_page_links, options, cookie_result, DETECT_LIST, LOCK, driver.current_url, START_OPTIONS["previous_packet_count"],
    ANALYSIS_DATA))  # driver 전달 시 에러. (프로세스간 셀레니움 공유가 안되는듯 보임)
    START_OPTIONS["previous_packet_count"] += len(packet_obj.packets)
    p.start()
    PROCESS_LIST.append(p)

    if len(PROCESS_LIST) > 3:
        for process in PROCESS_LIST:
            process.join()
        PROCESS_LIST = list()

    if depth == 0:
        return

    for visit_url in cur_page_links:
        if visit_url in START_OPTIONS["visited_links"]:
            continue
        if not func.isSameDomain(START_OPTIONS["input_url"], visit_url):
            continue
        if func.isSamePath(visit_url, START_OPTIONS["visited_links"]):
            continue
        if func.isExistExtension(visit_url, ["image"]):
            continue
        if checkCountLink(visit_url, START_OPTIONS["count_links"]):
            continue

        START_OPTIONS["visited_links"].append(visit_url)
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
        START_OPTIONS["count_links"][visit_path] = {"count": 1}

    return False


'''
    String visit_url: 입력한 url
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
