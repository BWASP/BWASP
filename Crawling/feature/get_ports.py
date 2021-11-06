import requests, re
from urllib.parse import urlparse
from socket import *
from bs4 import BeautifulSoup

def getPortsOnline(target_ip):
    open_ports = dict()
    pattern = re.compile('''^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\:(\d)+)?$''')
    if pattern.match(target_ip) is None:
        try:
            target_ip = gethostbyname(urlparse(target_ip).netloc)
        except:
            return open_ports
    
    html = BeautifulSoup(requests.get("https://search.censys.io/hosts/" + target_ip).text, features="html.parser")

    for i in html.select('h2'):
        port = i.get_text().replace('\n','').split('/')[0]
        port_num = port.replace(" ", "")
        port_service = i.get_text().replace('\n','').split('/')[1].split(" ")[0]

        open_ports[str(port_num)] = port_service

        #try:
        #    service = getservbyport(int(port))
        #    open_ports[str(port)] = service
        #except:
        #    open_ports[str(port)] = "Unknown"

    return open_ports

def getPortsOffline(target_ip):
    opened_ports = dict()
    pattern = re.compile('''^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\:(\d)+)?$''')
    if re.search(pattern, target_ip):
        try:
            print(urlparse(target_ip).netloc)
            target_ip = gethostbyname(urlparse(target_ip).netloc)
            target_port = 80
        except:
            return opened_ports
    else:
        target_ip = urlparse(target_ip).netloc
        target_port = 80
    
    if ":" in target_ip:
        target_ip, target_port = target_ip.split(':')
    
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect((target_ip,int(target_port)))
        ipscan = s.getsockname()[0]

        print("[+] IP : " +ipscan)

        port = [80, 8080, 443, 20, 21, 22, 23, 25, 53, 5357, 110, 123, 161, 1433, 3306, 1521, 135, 139, 137, 138, 445, 514, 8443, 3389, 8090, 42, 70, 79, 88, 118, 156, 220]

        service_data = {'3306': 'mysql', '1521': 'oracle', '8080': 'tomcat', '8443': 'https', '8090': 'tomcat', '220': 'imap3'}

        for p in port:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, p))
            try:
                service = getservbyport(p)
            except:
                p = str(p)
                service = service_data[""+p+""]
            
            if result == 0:
                opened_ports[str(p)] = service
                
    except Exception as e:
        print("[Error] - Port Scan\n" + str(e))
    
    return opened_ports

if __name__ == '__main__':
    print(getPortsOnline('http://9ucc1.xyz/8081').keys())