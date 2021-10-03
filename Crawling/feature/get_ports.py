import requests
from bs4 import BeautifulSoup

def getPorts(target_ip):
    open_ports = list()
    html = BeautifulSoup(requests.get("https://censys.io/ipv4/" + target_ip).text, features="html.parser")

    for i in html.select('h2'):
        open_ports.append(i.get_text().replace('\n','').split('/')[0])

    return open_ports


if __name__ == '__main__':
    print(getPorts('158.247.214.182'))