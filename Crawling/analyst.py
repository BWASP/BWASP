from Crawling.attack import webserver
from Crawling.attack import backend
from Crawling.attack import frontend


def start(target_url, req_res_packets, cur_page_links, page_source, current_url, options):
    return_data = {
        "webserver": webserver.getWebServerInfo(target_url, req_res_packets, options["server"]),
        "backend": backend.resBackend(current_url, page_source, req_res_packets, options["backend"]),
        "frontend": frontend.detectWebServer(target_url, cur_page_links, req_res_packets, options["framework"])
    }

    return return_data
