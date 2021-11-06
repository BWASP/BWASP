from Crawling.attack import sysinfo

def start(detect_list,lock,target_url, req_res_packets, cur_page_links,current_url, packet_indexes,options):
    return sysinfo.start(detect_list,lock,target_url, cur_page_links,current_url, req_res_packets,packet_indexes,options["framework"])