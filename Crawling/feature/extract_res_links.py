from seleniumwire import webdriver
from urllib.parse import urlparse
from urllib.parse import urljoin
import re

res_contlist=["javascript","json","xml"]
res_extlist=["js","xml"]
res_urllist=set()
res_exturllist=set()
res_jsonlist=set()
res_jslist=set()
res_xmllist=set()
res_htmllist=set()

def getExtraurl(main_url,body,url):
    #url regular expression
    #참고 정규식 pattern = re.compile('(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?z')
    #pattern = re.compile('(http|https)):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?')
    pattern = re.compile('((?:http|ftp|https)(?:://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)')
    prefix = urlparse(url).scheme+"://"
    for line in pattern.findall(body):
        if not "http" in line[0]:
            res_exturllist.add(prefix+line[0])
        else:
            res_exturllist.add(line[0])

def getjsExtraurl(main_url,body,url):
    # location 포함 확인 pattern = re.compile('''(location.href)\s*[=\(]\s*["']["'\.\w\/\\\?=&\s\+]+;)''')
    # location url 추출 
    #pattern = re.compile('''location.href\s*[=\(]\s*["'](["'\.\w\/\\\?=&\s\+]+);''')
    pattern = re.compile('''location.href\s*[=\(]\s*["'](["'_.,:\w\/\\\@?^=%&/~+#-]+);?''')
    #print("추출된 url",pattern.findall(body))
    for line in pattern.findall(body):
        line = re.sub('[\"\'\s+]','',line)
        # urljoin을 통해 ./  ../  / 와 같은 상대경로 문제 해결
        res_exturllist.add(urljoin(main_url,line))

            
#url 구분 저장 
def saveUrl(main_url,type,body,url):
    if type == "currentpage":
        res_htmllist.add(url)
        getExtraurl(main_url,body,url)
    # 확장자 일 경우 확장자에 따라 타입 정하기
    if type == "ext":
        extension=list()
        extension.append(urlparse(url).path.split(".")[-1])
        #index.php?page=a.xml 과 같은 경우 고려
        extension.append(urlparse(url).query.split("."[-1]))
        if "json" in extension:
            type="json"
        elif "js" in extension:
            type="javasript"
        elif "xml" in extension:
            type="xml"
    if type == "json":
            res_jsonlist.add(url)
            getExtraurl(main_url,body,url)
    if type =="javascript":
            res_jslist.add(url)
            getExtraurl(main_url,body,url)
            getjsExtraurl(main_url,body,url)
    if type =="xml":
            res_xmllist.add(url)
            getExtraurl(main_url,body,url)

def eachgetUrl(main_url,response,response_url):   
    if "content-type" in response["headers"]:
        content = response["headers"]["content-type"]
        for  contlist in res_contlist:
            if contlist in content:
                saveUrl(main_url,contlist,response["body"],response_url)
                break
    elif  "." in response_url:
        saveUrl(main_url,"ext",response["body"],response_url)

#Call this to get extra link
#res_geturl.start(driver.current_url, req_res_packets,driver.page_source)
def start(main_url,req_res_packet,page_source):
    saveUrl(main_url,"currentpage",page_source,main_url)
    for request in req_res_packet:
        # 탐색된 모든 url 저장
        #res_urllist.add(request[i]["request"]["url"])
        eachgetUrl(main_url,request["response"],request["request"]["full_url"])
    return sorted(list(res_exturllist))

def printUrl():
    print("res url link result : ")
    for result in sorted(list(res_urllist)):
        print(result)
    print("extra url link result :")
    # 받아오는 게 아직 불완전함 
    for result in sorted(list(res_exturllist)):
        print(result)
        

if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    # other chrome options
    chrome_options.add_argument('--headless')
    options = {
    'disable_encoding': True  # Tell the server not to compress the response
        }
    driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options,seleniumwire_options=options)
    URL = "https://twitter.com"
    driver.get(URL)
    for request in driver.requests:
        if(request.response):
            # 탐색된 모든 url 저장
            res_urllist.add(request.url)
            eachgetUrl(request.response,request.url)
    printUrl()
    driver.quit()