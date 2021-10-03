from seleniumwire import webdriver
from urllib.parse import urlparse

from feature import clickable_tags
from feature import packet_capture
from feature import res_geturl

def start(url, depth):
    driver = initSelenium()
    visit(driver, url, set([url]), depth)

def visit(driver, url, previous_url, depth):
    if depth == 0:
        return
    
    driver.get(url)

    req_res_packets = packet_capture.packetCapture(driver)
    cur_page_links = clickable_tags.bs4Crawling(url, req_res_packets)
    cur_page_links += res_geturl.getUrl(url, req_res_packets)
    
    # packet_capture.writeFile(req_res_packets)

    for visit_url in cur_page_links:
        if visit_url in previous_url:
            continue
        if not isSameDomain(url, visit_url):
            continue
        visit(driver, visit_url, previous_url.union(cur_page_links), depth-1)

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

def initSelenium():
    options = {
        "disable_encoding" : True
    }
    driver = webdriver.Chrome("./config/chromedriver.exe", seleniumwire_options = options)
    return driver

if __name__ == "__main__":
    url = "https://naver.com/"
    start(url, 2)