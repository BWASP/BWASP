from seleniumwire import webdriver
from seleniumwire.utils import decode
from urllib.parse import urlparse
import json

def webdriverSetting():
    # [*] If you want to get decoded response body, you have to add below option.
    options = {
        'disable_encoding': True,
        "detach" : True
    }
    driver = webdriver.Chrome("./chromedriver.exe", seleniumwire_options = options)
    return driver

def packetCapture(driver):
    network_packet = []
    for data in driver.requests:
        if data.response:
            network_packet.append({
                "request" : getRequestPacket(data), 
                "response" : getResponsePacket(data.response)
            })
        else:
            print("[!] Something Wrong.")

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

    return_data = { 
        "method" : data.method, 
        "url" : req_uri, 
        "headers" : {},
        "body" : ""
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
    
    try:
        body = decode(data.body, data.headers.get('Content-Encoding', 'identity'))
        return_data["body"] = body.decode('utf-8')

    except UnicodeDecodeError as e:
        # [*] Do not save image data...etc..
        print("UnicodeDecodeError: " + str(e))
    
    for x in str(data.headers).splitlines():
        data = x.split(": ")
        try: return_data["headers"][data[0].lower()] = data[1]
        except: pass
    
    return return_data

def writeFile(data):
    f = open("test.json", "w")
    json.dump(data, f, indent=4)
    f.close()

if __name__ == "__main__":
    # [!] You need to install the seleniumwire's root certificate. Visit below link.
    #     SSL Error: https://github.com/wkeeling/selenium-wire#certificates

    driver = webdriverSetting()
    url = "https://youtube.com"
    # driver.scopes = [
    #     '.*youtube.*'
    # ]

    driver.get(url)
    writeFile(packetCapture(driver))