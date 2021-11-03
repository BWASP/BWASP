from seleniumwire import webdriver
from seleniumwire.utils import decode
from urllib.parse import urlparse, urlunparse
import json

content_image_type = ["image/bmp", "image/cis-cod", "image/gif", "image/ief", "image/jpeg", "image/pipeg", "image/svg+xml", "image/tiff", "image/tiff", "image/png", "font/woff2"]

def webdriverSetting():
    # [*] If you want to get decoded response body, you have to add below option.
    options = {
        'disable_encoding': True,
        "detach" : True
    }
    driver = webdriver.Chrome("./config/chromedriver.exe", seleniumwire_options = options)
    return driver

def start(driver):
    network_packet = []
    for data in driver.requests:
        if data.response:
            if data.url == "https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard":
                continue

            network_packet.append({
                "request" : getRequestPacket(data), 
                "response" : getResponsePacket(data.response)
            })
        else:
            print("[!] Response is empty.")

    return network_packet

def getRequestPacket(data):
    parsed_url = urlparse(data.url)

    req_uri = parsed_url.path
    if parsed_url.query:
        req_uri += "?" + parsed_url.query
    if parsed_url.fragment:
        req_uri += "#" + parsed_url.fragment

    req_headers = ""
    if data.headers["host"] is None:
        req_headers = "host: {}\n{}".format(parsed_url.netloc, str(data.headers))
    else:
        req_headers = str(data.headers)

    # TODO
    # request body 넣기
    # https://pypi.org/project/selenium-wire/#example-update-json-in-a-post-request-body
    return_data = { 
        "method" : data.method, 
        "url" : req_uri, 
        "headers" : {},
        "body" : "",
        "full_url" : data.url 
    }

    for x in req_headers.splitlines():
        header = x.split(": ")
        try: return_data["headers"][header[0].lower()] = header[1]
        except: pass
    
    try:
        body = decode(data.body, data.headers.get('Content-Encoding', 'identity'))
        return_data["body"] = body.decode('utf-8')

    except UnicodeDecodeError as e:
        # [*] Do not save image data...etc..
        print("UnicodeDecodeError: " + str(e))

    return return_data

def getResponsePacket(data):
    return_data = {
        "headers" : {}, 
        "body" : "",
        "status_code" : data.status_code
    }
    
    for x in str(data.headers).splitlines():
        header = x.split(": ")
        try: return_data["headers"][header[0].lower()] = header[1]
        except: pass

    try:
        body = decode(data.body, data.headers.get('Content-Encoding', 'identity'))
        return_data["body"] = body.decode('utf-8')

    except UnicodeDecodeError as e:        
        if "content-type" in return_data["headers"].keys():
            if return_data["headers"]["content-type"] in content_image_type:
                return return_data

        body = decode(data.body, data.headers.get('Content-Encoding', 'identity'))
        return_data["body"] = body.decode("ISO-8859-1")

    except UnicodeDecodeError as e:
        # [*] Do not save image data...etc..
        print("UnicodeDecodeError: " + str(e))
    
    return return_data

"""
    This function filter only same domain when browser was redirected other site.
        - packets:      list (req, res packet)
        - target_url:   String

        - return:       list (req, res packet)
"""
def filterDomain(packets, target_url):
    target_domain = urlparse(target_url).netloc
    result_packet = []

    for packet in packets:
        if packet["request"]["headers"]["host"] == target_domain:
            result_packet.append(packet)
    
    return result_packet

def deleteFragment(links):
    for i in range(len(links)):
        parse = urlparse(links[i])
        parse = parse._replace(fragment="")
        links[i] = urlunparse(parse)

    return links

def deleteUselessBody(packets):
    content_types = ["text/css", "application/font-woff2"]

    for index in range(len(packets)):
        if "content-type" in list(packets[index]["response"]["headers"].keys()):
            for type in content_types:
                if packets[index]["response"]["headers"]["content-type"].find(type) != -1:
                    packets[index]["response"]["body"] = ""

    return packets

def writeFile(data):
    f = open("test.json", "w")
    json.dump(data, f, indent=4)
    f.close()

if __name__ == "__main__":
    # [!] You need to install the seleniumwire's root certificate. Visit below link.
    #     SSL Error: https://github.com/wkeeling/selenium-wire#certificates

    driver = webdriverSetting()
    url = "https://kitribob.kr"
    # driver.scopes = [
    #     '.*youtube.*'
    # ]

    driver.get(url)
    writeFile(start(driver))