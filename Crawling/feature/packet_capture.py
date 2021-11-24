from seleniumwire.utils import decode
from urllib.parse import urlparse, urlunparse
import json

class PacketCapture:

    def __init__(self):
        self.packets = list()
    
    def start(self, driver):
        for data in driver.requests:
            if data.response:
                if data.url == "https://accounts.google.com/ListAccounts?gpsia=1&source=ChromiumBrowser&json=standard":
                    continue

                self.packets.append({
                    "request" : self.getRequestPacket(data), 
                    "response" : self.getResponsePacket(data.response)
                })
            else:
                print("[!] Response is empty.")

        del driver.requests
    

    def getRequestPacket(self, request):
        parsed_url = urlparse(request.url)

        req_uri = parsed_url.path
        if parsed_url.query:
            req_uri += "?" + parsed_url.query
        if parsed_url.fragment:
            req_uri += "#" + parsed_url.fragment

        # Host 헤더 존재 여부 확인
        req_headers = ""
        if request.headers["host"] is None:
            req_headers = "host: {}\n{}".format(parsed_url.netloc, str(request.headers))
        else:
            req_headers = str(request.headers)

        # TODO
        # request body 넣기 https://pypi.org/project/selenium-wire/#example-update-json-in-a-post-request-body
        return_data = { 
            "method" : request.method, 
            "url" : req_uri, 
            "headers" : {},
            "body" : "",
            "full_url" : request.url 
        }

        # header key를 소문자로 바꾸기
        return_data["headers"] = self.headerKeyToLower(req_headers)
        
        # request body 디코딩
        try:
            body = decode(request.body, request.headers.get('Content-Encoding', 'identity'))
            return_data["body"] = body.decode('utf-8')

        except UnicodeDecodeError as e:
            # [*] Do not save image data...etc..
            print("UnicodeDecodeError: " + str(e))

        return return_data
    

    def getResponsePacket(self, response):
        filter_content_type_list = ["image/bmp", "image/cis-cod", "image/gif", "image/ief", "image/jpeg", "image/pipeg", "image/svg+xml", "image/tiff", "image/tiff", "image/png", "font/woff2"]
        return_data = {
            "headers" : {}, 
            "body" : "",
            "status_code" : response.status_code
        }
        
        # header key를 소문자로 바꾸기
        return_data["headers"] = self.headerKeyToLower(str(response.headers))

        try:
            body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
            return_data["body"] = body.decode('utf-8')

        except UnicodeDecodeError as e:        
            if "content-type" in return_data["headers"].keys():
                if return_data["headers"]["content-type"] in filter_content_type_list:
                    return return_data

            body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
            return_data["body"] = body.decode("ISO-8859-1")

        except UnicodeDecodeError as e:
            # [*] Do not save image data...etc..
            print("UnicodeDecodeError: " + str(e))
        
        return return_data
    

    def deleteUselessBody(self):
        content_types = ["text/css", "application/font-woff2"]

        for index in range(len(self.packets)):
            if "content-type" in list(self.packets[index]["response"]["headers"].keys()):
                for type in content_types:
                    if self.packets[index]["response"]["headers"]["content-type"].find(type) != -1:
                        self.packets[index]["response"]["body"] = ""
    

    def deleteFragment(self, links):
        for index in range(len(links)):
            parse = urlparse(links[index])
            parse = parse._replace(fragment="")
            links[index] = urlunparse(parse)

        return links
    

    """
    This function filter only same domain when browser was redirected other site.
        - packets:      list (req, res packet)
        - visited_url:   String

        - return:       list (req, res packet)
    """
    def filterPath(self, visited_url):
        for packet in self.packets:
            if packet["request"]["full_url"] == visited_url:
                self.packets = list()
                self.packets.append(packet)
                break
    

    def headerKeyToLower(self, headers):
        return_data = {}

        for header in headers.splitlines():
            header_info = header.split(": ")
            try: return_data[header_info[0].lower()] = header_info[1]
            except: pass
        
        return return_data


    def packetsToFile(self):
        f = open("test.json", "w")
        json.dump(self.packets, f, indent=4)
        f.close()