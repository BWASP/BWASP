import requests, re
from urllib.parse import urlparse
from socket import *
from bs4 import BeautifulSoup


class GetPort:
    def __init__(self):
        self.ports_list = dict()  # if port is open, get in
        self.wellKnown_ports = [80, 8080, 443, 20, 21, 22, 23, 25, 53, 5357, 110, 123, 161, 1433, 3306, 1521, 135, 139, 137, 138, 445, 514, 8443, 3389, 8090, 42, 70, 79, 88, 118,
                                156, 220]
        self.service_of_port = {'3306': 'mysql', '1521': 'oracle', '8080': 'tomcat', '8443': 'https', '8090': 'tomcat', '220': 'imap3'}

        self.port_pattern = re.compile('''^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\:(\d)+)?$''')
        self.port_scan = {
            "online": {
                "Get_port_information_url": "https://search.censys.io/hosts/",
                "target_ip": "",
                "target_ipv4": ""
            },
            "offline": {
                "target_ip": "",
                "target_ipv4": "",
                "target_port": 80
            }
        }

    def getPortsOnline(self, target_ip):
        if self.port_pattern.match(target_ip) is None:
            try:
                target_ip = gethostbyname(urlparse(target_ip).netloc)
            except:
                return self.ports_list

        parse_html = BeautifulSoup(
            requests.get(self.port_scan["online"]["Get_port_information_url"] + target_ip).text,
            features="html.parser")

        for select_idx in parse_html.select('h2'):
            port_data = select_idx.get_text().replace('\n', '').split('/')[0]
            port_number = port_data.replace(" ", "")
            port_service = select_idx.get_text().replace('\n', '').split('/')[1].split(" ")[0]

            self.ports_list[str(port_number)] = port_service

        return self.ports_list

    def getPortsOffline(self, target_ip):
        if re.search(self.port_pattern, target_ip):
            try:
                print(urlparse(target_ip).netloc)
                target_ip = gethostbyname(urlparse(target_ip).netloc)
                target_port = 80
            except:
                return self.ports_list
        else:
            target_ip = urlparse(target_ip).netloc
            target_port = 80

        if ":" in target_ip:
            target_ip, target_port = target_ip.split(':')

        try:
            s = socket(AF_INET, SOCK_DGRAM)
            s.connect((target_ip, int(target_port)))
            ipscan = s.getsockname()[0]

            print("[+] IP : " + ipscan)

            for p in self.wellKnown_ports:
                sock = socket(AF_INET, SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, p))

                try:
                    service = getservbyport(p)
                except:
                    p = str(p)
                    service = self.service_of_port["" + p + ""]

                if result == 0:
                    self.ports_list[str(p)] = service

        except Exception as e:
            print("[Error] - Port Scan\n" + str(e))

        return self.ports_list
