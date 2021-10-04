from seleniumwire import webdriver
from urllib.parse import urlparse, urlunparse

from feature import clickable_tags
from feature import packet_capture
from feature import res_geturl

check = True
input_url = ""
visited_links = []

def start(url, depth):
    driver = initSelenium()

    visit(driver, url, depth)

def visit(driver, url, depth):
    global check
    global input_url
    global visited_links

    driver.get(url)

    if check:
        input_url = driver.current_url
        visited_links.append(input_url)
        check = False

    req_res_packets = packet_capture.packetCapture(driver)
    cur_page_links = clickable_tags.bs4Crawling(driver.current_url, driver.page_source)
    cur_page_links += res_geturl.getUrl(driver.current_url, req_res_packets)
    cur_page_links = list(set(deleteFragment(cur_page_links)))

    # print(input_url)
    # print(cur_page_links)
    # print(depth)

    ################################
    #### Add Attack Vector Code ####
    ################################
    if depth == 0:
        return

    for visit_url in cur_page_links:
        if visit_url in visited_links:
            continue
        if not isSameDomain(input_url, visit_url):
            # print("notSameDomain: {}".format(visit_url))
            continue
        if isSamePath(visit_url, visited_links):
            continue
        # print("visit: {}".format(visit_url))
        # input("")

        visited_links.append(visit_url)
        visit(driver, visit_url, depth-1)

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

def isSamePath(visit_url, previous_urls):
    try:
        visit = urlparse(visit_url)

        for link in previous_urls:
            previous = urlparse(link)

            if (visit.path == previous.path) and (visit.query == previous.query):
                print("[!] SamePath: {} {}".format(visit_url, link))
                return True
        else:
            print("[!] Not SamePath: {}".format(visit_url))
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
    url = "https://kitribob.kr/"
    start(url, 10)