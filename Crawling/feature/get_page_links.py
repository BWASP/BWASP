# https://marketology.co.kr/all-category/tag_type-manager/gtm-%ED%81%B4%EB%A6%AD-%EC%9D%B4%EB%B2%A4%ED%8A%B8-%EC%B6%94%EC%A0%81%EC%9D%98-%EC%A0%95%EC%9D%98-%EB%AA%A9%EC%A0%81-%EB%B0%A9%EB%B2%95/
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class GetPageLinks:
    def __init__(self, url, page_source):
        self.page_source = BeautifulSoup(page_source, features="html.parser")
        self.tag_type_list = ['button','a','div','img','input'] 
        self.url = url

    # 2. BeautifulSoup을 이용한 태그 클릭 리스트
    def start(self):
        cur_page_links = list()

        # page source 내에 tag_type 해당하는 태그 있는지 검사
        for tag_type in self.tag_type_list:
            for tag in self.page_source.find_all(tag_type): # tag_type 에 해당하는 tag 하나하나 접근
                if 'href' in tag.attrs: # tag에 href atrribute가 존재하는지 확인
                    cur_page_links.append(urljoin(self.url, tag.attrs['href']))
        return cur_page_links


if __name__ == "__main__":
    import ast, json
    url = "http://suninatas.com/"
    req_res_packets = json.loads(open('./test.json','r').read())
    for packet in req_res_packets:
        print(GetPageLinks(url, packet['response']['body']).start())
        input()