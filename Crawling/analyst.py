from Crawling.attack import sysinfo


def start(target_url, req_res_packets, cur_page_links, options):
    return sysinfo.start(target_url, cur_page_links, req_res_packets,options["framework"])