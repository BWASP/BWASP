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

URL = "http://twitter.com"
driver.get(URL)

#url 받을시 형태에 따라 저장 
def save_url(url):
    res_urllist.add(url)
    if "." in url:
        if url.split(".")[-1] == "json":
            res_jsonlist.add(url)
        elif url.split(".")[-1] == "json":
            res_jslist.add(url)

#reponse에서 확장자 
def get_url(response,response_url):
    content = request.response.headers['Content-Type']
    if  "." in response_url:
        save_url(response_url)
    elif content and (res_contlist[0] in content):
        save_url(response_url)


#netwrok response 안의 패킷 분석
def get_extra_url(body,url):
    #url regular expression
    pattern = re.compile('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
    print(url)
    #print(body.decode("utf8"))
    print("-"*10,"body's url start")
    for line in pattern.findall(body.decode("utf8")):
        print(line)
    print("-"*10,"body's url end")

for request in driver.requests:
    if(request.response):
        get_url(request.response,request.url)
        get_extra_url(request.response.body,request.url)

for list in sorted(list(res_urllist)):
    print(list)        
driver.quit()