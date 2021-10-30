from Crawling.attack import webserver
from Crawling.attack import backend
from Crawling.attack import frontend
from Crawling.attack import sysinfo

def start(target_url, req_res_packets, cur_page_links, driver, options):
    return sysinfo.start(target_url, cur_page_links, req_res_packets,options["framework"])