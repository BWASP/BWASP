from attack import webserver
from attack import backend
from attack import frontend

def start(target_url, req_res_packets, cur_page_links, driver):
    return_data = {
        "webserver" : webserver.getWebServerInfo(target_url, req_res_packets),
        "backend" : backend.resBackend(driver, req_res_packets),
        "frontend" : frontend.detectWebServer(target_url, cur_page_links, req_res_packets, driver)
    }

    return return_data