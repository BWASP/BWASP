from seleniumwire import webdriver
import re


#respone allow contenttype list
#response allow extension list 
res_contlist=[]
res_extlist=[".js"]

options = {
    'disable_encoding': True  # Tell the server not to compress the response
        }

# other chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options,seleniumwire_options=options)

URL = "http://twitter.com"
driver.get(URL)


pattern = re.compile('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')
cot_type=set([])
for request in driver.requests:
    #print(request.url)
    #if "js" in request.url:
    content = request.response.headers['Content-Type']
    if(content):
        if "javascript" in content :
            print(request.url)
            #print(request.response.body.decode("utf8"))

            for line in pattern.findall(request.response.body.decode("utf8")):
                print(line)

driver.quit()

'''if(request.response.headers['Content-Type']):
        cot_type.add(request.response.headers['Content-Type'])
print(cot_type)
cot_type=list(cot_type)

filename = URL+".txt"
filename=filename.replace("https://","")
filename=filename.replace("http://:","")
filename=filename.replace("/","")
f = open(filename,"w")
for i in range(len(cot_type)):
    f.write(cot_type[i].replace(";","\n"))
f.close()
'''