# https://marketology.co.kr/all-category/tag-manager/gtm-%ED%81%B4%EB%A6%AD-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%B6%94%EC%A0%81%EC%9D%98-%EC%A0%95%EC%9D%98-%EB%AA%A9%EC%A0%81-%EB%B0%A9%EB%B2%95/

import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
def parsingURL(url):
    parsed_url = urlparse(url)
    req_uri = parsed_url.netloc + parsed_url.path
    if parsed_url.query:
        req_uri += "?" + parsed_url.query
    if parsed_url.fragment:
        req_uri += "#" + parsed_url.fragment
    
    return req_uri
'''

def seleniumSetting(url):
    driver = webdriver.Chrome('/Users/dohunny/MyDoc/Data2021/BoB/Project/BWASP_dev/chromedriver')
    driver.get(url)
    return driver


# 1. Selenium을 이용한 태그 클릭
def seleniumCrawling(driver):

    # 가져올 태그 목록
    clickable_tag_list = ['button','a','div','img','input'] 
    cur_page_links, elems = list(), list()

    for tag in clickable_tag_list:
        # 찾을 tag가 전부 로드 될 때까지 기다리기
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,tag))
        )
        
        # 찾을 tag에 해당하는 element를 리스트에 append
        elems.append(driver.find_elements_by_tag_name(tag))

    for index in range(len(elems)):
        for elem in elems[index]:
            req_url = elem.get_attribute('href')
            
            # Selenium 사용 시, element 클릭 가능 여부 판단 방법 ( HTML 내부에서 클릭 이벤트가 구현되어있는 경우, 태그 속성 중 href가 존재 )
            if req_url is not None:
                cur_page_links.append(req_url)

                # print(elem.get_attribute('outerHTML')) # 태그를 text 형식으로 출력 (Ex: <a href="mail.naver.com">메일</a>)

    print(cur_page_links)
    return cur_page_links


# 2. BeautifulSoup을 이용한 태그 클릭 리스트
def bs4Crawling(url):
    html = requests.get(url).text

    soup = BeautifulSoup(html, features="html.parser")

    tags = list()

    tags.append(soup.find_all('a'))
    tags.append(soup.find_all('button'))
    tags.append(soup.find_all('img'))
    tags.append(soup.find_all('div'))
    tags.append(soup.find_all('input'))

    a_href_list = list()

    for index in range(len(tags)):
        for item in tags[index]:
            try:
                if item['href']:
                    a_href_list.append(item['href'])
            except KeyError as e:
                print(e)

    # print(a_href_list)
    return a_href_list


if __name__ == "__main__":
    url = "https://www.naver.com/"
    driver = seleniumSetting(url)
    seleniumCrawling(driver)