from seleniumwire import webdriver

import clickable_tags
import packet_capture
import res_geturl

def start(url, depth):
    driver = initSelenium()
    visit(driver, url, set(), depth)

def visit(driver, url, previous_url, depth):
    if depth == 0:
        return
    
    driver.get(url)

    cur_page_links = clickable_tags.seleniumCrawling(driver)
    req_res_packets = packet_capture.packetCapture(driver)
    cur_page_links.append(res_geturl.getUrl(req_res_packets))

    for url in cur_page_links:
        if url in previous_url:
            continue
        else:
            visit(driver, url, previous_url.add(cur_page_links), depth-1)

def initSelenium():
    options = {
        "disable_encoding" : True
    }
    driver = webdriver.Chrome("./chromedriver.exe", seleniumwire_options = options)
    return driver

if __name__ == "__main__":
    url = "https://naver.com"
    start(url)