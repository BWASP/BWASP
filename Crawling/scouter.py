from seleniumwire import webdriver
from urllib.parse import urlparse, urlunparse

from Crawling import analyst
from Crawling.feature import get_page_links, packet_capture, get_res_links, get_ports, get_cookies, get_domains, csp_evaluator, db, func

start_options = {
    "check" : True,
    "input_url" : "",
    "visited_links" : []
}

def start(url, depth, options):
    driver = initSelenium()
    visit(driver, url, depth, options)
    driver.quit()

def visit(driver, url, depth, options):
    global start_options

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
    
    analyst_result = analyst.start(start_options["input_url"], req_res_packets, cur_page_links, driver, options['info'])
    req_res_packets = packet_capture.deleteUselessBody(req_res_packets)

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
        # 무한 크롤링 해결 해야 함.
        start_options["visited_links"].append(visit_url)
        visit(driver, visit_url, depth - 1, options)

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
