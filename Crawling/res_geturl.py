from seleniumwire import webdriver
from urllib.parse import urlparse
import re

res_contlist=["javascript","json"]
res_extlist=["js"]
res_urllist=set()
res_exturllist=set()
res_jsonlist=set()
res_jslist=set()

def getExtraurl(body,url):
    #url regular expression
    #참고 정규식 pattern = re.compile('(http|ftp|https)(://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?z')
    #pattern = re.compile('(http|https)):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?')
    pattern = re.compile('(?:http|ftp|https)(?://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?z')
    

    for line in pattern.findall(body):
        print("extra link ","".join(line))
        res_exturllist.add("".join(line))
            
#url 구분 저장 
def saveUrl(type,body,url):
    # 확장자 일 경우 확장자에 따라 타입 정하기
    if type == "ext":
        extension = url.split(".")[-1]
        if extension == "json":
            type="json"
        elif extension == "js":
            type="javasript"

    if type == "json":
            res_jsonlist.add(url)
            getExtraurl(body,url)

    if type =="javascript":
            res_jslist.add(url)
            getExtraurl(body,url)

def eachgetUrl(response,response_url):   
    if "content-type" in response["headers"]:
        content = response["headers"]["content-type"]
        for  contlist in res_contlist:
            if contlist in content:
                saveUrl(contlist,response["body"],response_url)
                break
    elif  "." in response_url:
        saveUrl("ext",response["body"],response_url)


#Call this to get extra link
def getUrl(req_res_packet):
    for i, request in enumerate(req_res_packet):
        # 탐색된 모든 url 저장
        #res_urllist.add(request[i]["request"]["url"])
        eachgetUrl(request[i]["response"],request[i]["request"]["url"])
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