from seleniumwire import webdriver
from urllib.parse import urlparse, urlunparse

from feature import clickable_tags
from feature import packet_capture
from feature import res_geturl

def start(url, depth):
    driver = initSelenium()
    visit(driver, url, set([url]), depth)

def visit(driver, url, previous_url, depth):
    driver.get(url)

    req_res_packets = packet_capture.packetCapture(driver)
    cur_page_links = clickable_tags.bs4Crawling(driver.current_url, driver.page_source)
    cur_page_links += res_geturl.getUrl(url, req_res_packets)
    cur_page_links = list(set(deleteFragment(cur_page_links)))

    ################################
    #### Add Attack Vector Code ####
    ################################
    if depth == 0:
        return

    for visit_url in cur_page_links:
        if visit_url in previous_url:
            continue
        if not isSameDomain(url, visit_url):
            continue
        visit(driver, visit_url, previous_url.union(cur_page_links), depth-1)

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

def deleteFragment(links):
    for i in range(len(links)):
        parse = urlparse(links[i])
        parse = parse._replace(fragment="")
        links[i] = urlunparse(parse)

    return links

def initSelenium():
    options = {
        "disable_encoding" : True
    }
    driver = webdriver.Chrome("./config/chromedriver.exe", seleniumwire_options = options)
    return driver

if __name__ == "__main__":
    url = "https://www.naver.com"
    start(url, 3)