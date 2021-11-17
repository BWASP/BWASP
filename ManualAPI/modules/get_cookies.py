import json, sys, os
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from modules.func import *


def start(url, req_res_packets):
    cookies_per_packet = dict()

    for packet in req_res_packets:
        cookies = dict()
        if not func.isSameDomain(url, packet["request"]["full_url"]) or "cookie" not in list(packet["request"]["headers"].keys()):
            continue

        for i in packet["request"]["headers"]["cookie"].split('; '):
            cookies[i.split('=')[0]] = i.split('=')[1]

        cookies_per_packet[packet["request"]["full_url"]] = cookies

    return cookies_per_packet


if __name__ == "__main__":
    req_res_packets = json.loads(open('./test.json', 'r').read())
    print(start('https://kitribob.kr/', req_res_packets))
