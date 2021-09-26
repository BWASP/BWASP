from seleniumwire import webdriver
from seleniumwire.utils import decode
from urllib.parse import urlparse
from pprint import pprint

def packetCapture(url):
    # [*] If you want to get decoded response body, you have to add below option.
    options = {
        'disable_encoding': True
    }
    driver = webdriver.Chrome("./chromedriver.exe", seleniumwire_options = options)
    driver.get(url)
    
    network_packet = []
    for i, data in enumerate(driver.requests):
        if data.response:
            network_packet.append({"request" : {}, "response" : {}})
            # network_packet[i]["request"] = getRequestPacket(data)
            network_packet[i]["response"] = getResponsePacket(data)
        else:
            print("[!] Something Wrong.")
        
        if i == 3:
            break

    pprint(network_packet)

    return network_packet

def getRequestPacket(data):
    """
     TODO
     -> request body
     -> HTTP protocol
    """
    parsed_url = urlparse(data.url)

    req_uri = parsed_url.path
    if parsed_url.query:
        req_uri += "?" + parsed_url.query
    if parsed_url.fragment:
        req_uri += "#" + parsed_url.fragment

    req_headers = ""
    if data.headers["Host"] is None:
        req_headers = "Host: {}\n{}".format(parsed_url.netloc, str(data.headers))
        # req_headers = "{} {}\r\n{}".format(data.method, req_uri, req_headers)

    return_data = {"headers" : {}, "method" : data.method, "url" : req_uri}
    for x in req_headers.splitlines():
        data = x.split(": ")
        try: return_data["headers"][data[0]] = data[1]
        except: pass
    
    return return_data

def getResponsePacket(data):
    """
     TODO
     -> status code
     -> HTTP protocol
    """

    return_data = {"headers" : {}, "body" : ""}

    try:
        body = decode(data.response.body, data.response.headers.get('Content-Encoding', 'identity'))
        return_data["body"] = body.decode('utf-8')

        for x in str(data.response.headers).splitlines():
            data = x.split(": ")
            try: return_data["headers"][data[0]] = data[1]
            except: pass
    except Exception as e:
        # [*] Do not save image data...etc..
        print("Exception: " + str(e))
    
    return return_data

if __name__ == "__main__":
    # [!] You need to install the seleniumwire's root certificate. Visit below link.
    #     SSL Error: https://github.com/wkeeling/selenium-wire#certificates
    url = "https://naver.com"
    packetCapture(url)