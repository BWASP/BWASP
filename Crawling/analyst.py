from attack import webserver
from attack import backend
from attack import frontend

def start(target_url, req_res_packets, cur_page_links, driver, options):
    return_data = {
        "webserver" : webserver.getWebServerInfo(target_url, req_res_packets, options["server"]),
        "backend" : backend.resBackend(driver, req_res_packets, options["backend"]),
        "frontend" : frontend.detectWebServer(target_url, cur_page_links, req_res_packets, driver, options["framework"])
    }

    return return_data