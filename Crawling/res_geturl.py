from seleniumwire import webdriver
import re


#respone allow contenttype list
#response allow extension list 
#response filtered url list 
res_contlist=["javascript","json"]
res_extlist=["js"]
res_urllist=set()
res_jsonlist=set()
res_jslist=set()

options = {
    'disable_encoding': True  # Tell the server not to compress the response
        }


#def make_extlist():
# other chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options,seleniumwire_options=options)

URL = "https://twitter.com/"
driver.get(URL)

#url 받을시 형태에 따라 저장 
#type 0=> 확장자로 구분
#type 1=> 확장자 불가 content-type으로 구분
#netwrok response 안의 패킷 분석

def getExtraurl(body,url):
    #url regular expression
    pattern = re.compile('(?:http|ftp|https)(?:://)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?z')
    #pattern = re.compile('(http|https)):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?')
    print(url)
    #print(body.decode("utf8"))
    print("-"*10,"body's url start")
    try:
        for line in pattern.findall(body.decode("utf8")):
            print("extra link ","".join(line))
            # regex group 에 따라 분리해서 출력 가능
            #print("why ",line[0]+"://"+line[1]+line[2])
    #utf-8이 오류날 경우        
    except:
         for line in pattern.findall(body.decode("ISO-8859-1")):
            print("extra link ","".join(line))
            # regex group 에 따라 분리해서 출력 가능
            #print("why ",line[0]+"://"+line[1]+line[2])


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
            print("json:"," ")
            getExtraurl(body,url)

    if type =="javascript":
            res_jsonlist.add(url)
            print("javascript:"," ")
            getExtraurl(body,url)



#reponse에서 js,json등 정해진 경우만 url 저장
def getUrl(response,response_url):
    content = request.response.headers['Content-Type']
    # 확장자 이상하지만 js , json일 경우 
    if content and (res_contlist[0] in content):
        for  contlist in res_contlist:
            if content in contlist:
                saveUrl(contlist,response.body,response_url)
                break
    elif  "." in response_url:
        saveUrl("ext",response.body,response_url)




for request in driver.requests:
    if(request.response):
        # 탐색된 모든 url 저장
        res_urllist.add(request.url)
        getUrl(request.response,request.url)

for list in sorted(list(res_urllist)):
    print(list)    
driver.quit()