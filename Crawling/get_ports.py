import requests
from bs4 import BeautifulSoup


def getSession():
    cookies = {"polito":"\"8fef2320ef0254a734ff3e0994310ccb6153acd26153a86adf1899e8b8fae872!\""}
    return cookies

def getPorts(target_ip):
    open_ports = list()

    html = BeautifulSoup(requests.get("https://www.shodan.io/host/" + target_ip, cookies=getSession()).text, features="html.parser")
    
    print(html)
    input()

    for a_tag in html.select('#ports > a'):
        print(a_tag.get_text())
        open_ports.append(a_tag.get_text())

    return open_ports


if __name__ == '__main__':
    print(getPorts('223.130.195.95'))