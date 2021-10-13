from urllib.parse import urlparse
from Crawling.feature import func

def start(domains_per_page, url, cur_page_links):
    visit_url_list = list()
    for visit_url in cur_page_links:
        if func.isSameDomain(url, visit_url):
            # target URL과 같은 도메인인지 판단 후, 같으면 처음으로, 다르면 밑의 내용 실행
            continue
        visit_url_list.append(visit_url)

    domains_per_page[url] = visit_url_list
    return domains_per_page

if __name__ == "__main__":
    url_list = ["https://kitribob.kr/", "https://kitribob.kr/intro/bi", "https://kitribob.kr/helloworld"]
    domains_per_page = dict() # {"https://kitribob.kr/":["https://google.com", "https://www.naver.com/", "https://cloudflare.net", ...]}
    cur_page_links = ["https://google.com","https://www.naver.com","https://cloudflare.net/","https://kitribob.kr/intro/bi"]
    for url in url_list:
        domains_per_page = start(domains_per_page, url, cur_page_links)
    
    print(domains_per_page)