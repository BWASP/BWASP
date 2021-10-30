from Crawling.attack import webserver
from Crawling.attack import backend
from Crawling.attack import frontend
from Crawling.attack import sysinfo


def start(target_url, req_res_packets, cur_page_links, driver, options):
   # return_data = {
   #    "webserver": webserver.getWebServerInfo(target_url, req_res_packets, options["server"]),
   #     "backend": backend.resBackend(driver, req_res_packets, options["backend"]),
   #     "frontend": frontend.detectWebServer(target_url, cur_page_links, req_res_packets, driver, options["framework"])
   #  }
    return sysinfo.start(target_url, cur_page_links, req_res_packets,options["framework"])


    #  서버에서 전송할때 카테고리까지 구분해서 보내 줄지  or  서버에서 보내주면 직접 카테고리 파악할지 (크게 무리 주지 않음)