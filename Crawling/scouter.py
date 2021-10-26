from seleniumwire import webdriver
from urllib.parse import urlparse, urlunparse

from Crawling import analyst
from Crawling.feature import get_page_links, packet_capture, get_res_links, get_ports, get_cookies, get_domains, csp_evaluator, db, func

def start(url, depth, options):
    driver = initSelenium()
    start_options = {
        "check" : True,
        "input_url" : "",
        "visited_links" : []
    }
    visit(driver, url, depth, options, start_options)
    driver.quit()

def visit(driver, url, depth, options, start_options):
    print("check: {}, input_url: {}, visited_links: {}".format(start_options["check"], start_options["input_url"], len(start_options["visited_links"])))
    try:
        driver.get(url)
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        pass

    if start_options["check"]:
        start_options["input_url"] = driver.current_url
        start_options["visited_links"].append(start_options["input_url"])
        start_options["check"] = False

        if "portScan" in options["tool"]["optionalJobs"]:
            target_port = get_ports.getPortsOnline(start_options["input_url"])
            db.insertPorts(target_port, start_options["input_url"])

    # TODO
    # 다른 사이트로 redirect 되었을 때, 추가적으로 same 도메인 인지를 검증하는 코드가 필요함.
    # 첫 패킷에 google 관련 패킷 지우기
    req_res_packets = packet_capture.start(driver)
    cur_page_links = get_page_links.start(driver.current_url, driver.page_source)
    cur_page_links += get_res_links.start(driver.current_url, req_res_packets, driver.page_source)
    cur_page_links = list(set(deleteFragment(cur_page_links)))
    
    cookie_result = get_cookies.start(driver.current_url, req_res_packets)
    domain_result = get_domains.start(dict(), driver.current_url, cur_page_links)

    if "CSPEvaluate" in options["tool"]["optionalJobs"]:
        csp_result = csp_evaluator.start(driver.current_url)
        db.insertCSP(csp_result)

    # TODO
    # 찾은 정보의 Icon 제공
    analyst_result = analyst.start(start_options["input_url"], req_res_packets, cur_page_links, driver, options['info'])

    req_res_packets = deleteCssBody(req_res_packets)

    previous_packet_count = db.getPacketsCount()
    db.insertPackets(req_res_packets)
    db.insertDomains(req_res_packets, cookie_result, previous_packet_count, driver.current_url)
    db.insertWebInfo(analyst_result, start_options["input_url"], previous_packet_count)
    # Here DB code 

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

        # TODO
        # target 외에 다른 사이트로 redirect 될때, 검증하는 코드 작성 필요
        # 무한 크롤링
        start_options["visited_links"].append(visit_url)
        visit(driver, visit_url, depth - 1, options, start_options)

def deleteFragment(links):
    for i in range(len(links)):
        parse = urlparse(links[i])
        parse = parse._replace(fragment="")
        links[i] = urlunparse(parse)

    return links

def deleteCssBody(packets):
    css_content_types = ["text/css"]

    for index in range(len(packets)):
        if "content-type" in list(packets[index]["response"]["headers"].keys()):
            for type in css_content_types:
                if packets[index]["response"]["headers"]["content-type"].find(type) != -1:
                    packets[index]["response"]["body"] = ""

    return packets


def initSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_experimental_option("prefs", {
        "download_restrictions": 3
    })
    options = {
        "disable_encoding": True
    }

    driver = webdriver.Chrome("./Crawling/config/chromedriver.exe", seleniumwire_options=options, chrome_options=chrome_options)
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
