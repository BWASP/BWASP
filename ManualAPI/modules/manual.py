#=========================== 나중에 다시 참고해야 할 것 ===============================
'''
start_options["previous_packet_count"] += len(req_res_packets)
recent_packet_count =  len(req_res_packets) + previous_packet_count
    # {"id": "[1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]"}     
    if len(loadpacket_indexes) < recent_packet_count:
        #수정 후 loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"])["id"]
        loadpacket_indexes = json.loads(Packets().GetAutomationIndex()["retData"]["id"])

        packet_indexes = loadpacket_indexes[previous_packet_count:recent_packet_count]
    #analyst_result = analyst.start(sysinfo_detectlist,input_url, req_res_packets, cur_page_links, packet_indexes,options['info'])
    # res_req_packet index는 0 부터 시작하는데 ,  해당 index가 4인경우 realted packet에 packet_indexes[4]로 넣으면 됨 

    loadpacket_indexes = list()  # automation packet indexes    
'''

import re
import json

from ManualAPI.modules import db, attack_vector, api


loadpacket_indexes = list()  # automation packet indexes

http_method = "None"
infor_vector = "None"
robots_result = False
error_result = False

current_url = "http://suninatas.com"

receive = {
  current_url: [
    {
      "request": "...",
      "response": "..."
    }
  ]
}



http_method, infor_vector = attackHeader(list(receive.keys())[0])
robots_result = robotsTxt(list(receive.keys())[0])
error_result = errorPage(list(receive.keys())[0])


req_res_packets = db.deleteUselessBody(receive[list(receive.keys())[0]][0])  # CRX 패킷을 deleteUselessBody 통과 되도록
cookie_result = get_cookies.start(list(receive.keys())[0], req_res_packets)

#
#req_res_packets = #자동쪽의 패킷 값 가져오게
#cookie_result = #자동쪽의 쿠키 값 가져오게
#

'''

'''

db.insertPackets(req_res_packets)
result = db.insertDomains(req_res_packets, cookie_result, packet_indexes, list(receive.keys())[0], http_method, infor_vector,
                 robots_result, error_result) 

print("CHECK 제발")
print(result)