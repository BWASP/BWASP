from seleniumwire import webdriver
from urllib.parse import urlparse
from urllib.parse import urljoin
import re


class GetReslinks:

    def __init__(self,main_url,req_res_packet,page_source):
        self.res_contlist=["javascript","json","xml"]
        self.res_extlist=["js","xml"]
        self.main_url = main_url
        self.req_res_packet = req_res_packet
        self.page_source = page_source

        self.res_exturllist=set()
        self.res_urllist=set()

        self.pattern = {
            "getExtraurl": re.compile('((?:http|ftp|https)(?:://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)'),
            "getjsExtraurl": re.compile('''location.href\s*[=\(]\s*["'](["'_.,:\w\/\\\@?^=%&/~+#-]+);?''')
        }
        

    def getExtraurl(self,body,url):
        #url regular expression
        #참고 정규식 pattern = re.compile('(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?z')
        #pattern = re.compile('(http|https)):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?')
        prefix = urlparse(url).scheme+"://"
        for line in self.pattern["getExtraurl"].findall(body):
            if not "http" in line[0]:
                self.res_exturllist.add(prefix+line[0])
            else:
                self.res_exturllist.add(line[0])

    #url은 디버깅 용도
    def getjsExtraurl(self,body,url):
        # location 포함 확인 pattern = re.compile('''(location.href)\s*[=\(]\s*["']["'\.\w\/\\\?=&\s\+]+;)''')
        # location url 추출 
        #pattern = re.compile('''location.href\s*[=\(]\s*["'](["'\.\w\/\\\?=&\s\+]+);''')
        pattern = re.compile('''location.href\s*[=\(]\s*["'](["'_.,:\w\/\\\@?^=%&/~+#-]+);?''')
        #print("추출된 url",pattern.findall(body))
        for line in self.pattern["getjsExtraurl"].findall(body):
            line = re.sub('[\"\'\s+]','',line)
            # urljoin을 통해 ./  ../  / 와 같은 상대경로 문제 해결
            self.res_exturllist.add(urljoin(self.main_url,line))

    def saveUrl(self,type,body,url):
        if type == "currentpage":
            self.getExtraurl(body,url)
        # 확장자 일 경우 확장자에 따라 타입 정하기
        if type == "ext":
            extension=list()
            extension.append(urlparse(url).path.split(".")[-1])
            #index.php?page=a.xml 과 같은 경우 고려
            extension.append(urlparse(url).query.split("."[-1]))
        #TODO  if extension type is different , executed method is different so simplifying is difficult     
            if "json" in extension:
                type="json"
            elif "js" in extension:
                type="javasript"
            elif "xml" in extension:
                type="xml"
        if type == "json":
                self.getExtraurl(body,url)
        if type =="javascript":
                self.getExtraurl(body,url)
                self.getjsExtraurl(body,url)
        if type =="xml":
                self.getExtraurl(body,url)

    def eachgetUrl(self,response,response_url):   
        if "content-type" in response["headers"]:
            content = response["headers"]["content-type"]
            for  contlist in self.res_contlist:
                if contlist in content:
                    self.saveUrl(contlist,response["body"],response_url)
                    break
        elif  "." in response_url:
            self.saveUrl("ext",response["body"],response_url)

    def printUrl(self):
        print("res url link result : ")
        for result in sorted(list(self.res_urllist)):
            print(result)
        print("extra url link result :")
        # 받아오는 게 아직 불완전함 
        for result in sorted(list(self.res_exturllist)):
            print(result)
    
    def ret_res_exturllist(self):
        return sorted(list(self.res_exturllist))

    def start(self):
        self.saveUrl("currentpage",self.page_source,self.main_url)
        for request in self.req_res_packet:
            # 탐색된 모든 url 저장
            #res_urllist.add(request[i]["request"]["url"])
            self.eachgetUrl(request["response"],request["request"]["full_url"])
        return sorted(list(self.res_exturllist))
