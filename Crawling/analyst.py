from Crawling.attack import sysinfo


def start(detect_list,target_url, req_res_packets, cur_page_links, options):
    return sysinfo.start(detect_list,target_url, cur_page_links, req_res_packets,options["framework"])