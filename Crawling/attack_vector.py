from bs4 import BeautifulSoup
import requests
import json


def attack_header(target_url):
    r = requests.get(target_url)
    dict_data = r.headers
    infor_data = ""
    infor_vector = ""
    http_method = requests.options(target_url)
    try:
        http_method = http_method.headers['Allow'].replace(",", "").split(" ")
    except:
        http_method = "private"

    try:
        tmp_data = dict_data['Set-Cookie']
        i = len(tmp_data.split())
        if "HttpOnly" in tmp_data:
            for j in range(0, i):
                infor_data += tmp_data.split()[j] + "\n"
        elif "Secure" in tmp_data:
            for j in range(0, i):
                infor_data += tmp_data.split()[j] + "\n"
        else:
            infor_data = tmp_data
            infor_vector += "Not_HttpOnly\n"

    except:
        infor_vector += "Not_HttpOnly\n"

    try:
        tmp_data = dict_data['X-Frame-Options']
        i = len(tmp_data.split())
        for j in range(0, i):
            infor_data += tmp_data.split()[j] + "\n"

    except:
        infor_vector += "Not_X-Frame-Options\n"

    return http_method, infor_vector


def input_tag(response_body, http_method, infor_vector):
    # form tag action and input tag and input name parse
    soup = BeautifulSoup(response_body, 'html.parser')

    tag_list = list()
    tag_name_list = list()
    action_page = list()
    action_type = list()

    attack_vector = list()

    data = dict()

    text = soup.find_all('input')
    form = soup.find_all('form')

    with open("./attack_vector.json", 'r', encoding='UTF8') as f:
        data = json.load(f)

    for tag in text:
        try:
            if tag.attrs['type'] != "submit" and len(text) != 0:
                tag_list.append(str(tag))  # input tag 값 ex) <input ~
                tag_name_list.append(tag.attrs['name'])

                #~~~~~~~~~~~~SQL Injection
                data[0]["vuln"] = "SQL Injection"
                data[0]["impactRate"] = 1

                # th tag check (board) and type="password" check (login)
                if "<th" in response_body:  # TODO: bs4 use
                    data[0]["Type"] = "board"
                    data[0]["impactRate"] = 2

                if tag.attrs['type'] == "password":
                    data[0]["Type"] = "account"
                    data[0]["impactRate"] = 2

                #~~~~~~~~~~~~XSS
                data[1]["vuln"] = "XSS"
                data[1]["impactRate"] = 1
                
                if "Not_HttpOnly" in infor_vector:
                    data[1]["Header"]["HttpOnly"] = False
                    data[1]["impactRate"] = 2
                elif "Not_X-Frame-Options" in infor_vector:
                    data[1]["Header"]["HttpOnly"] = False
                    data[1]["impactRate"] = 2

                
                #~~~~~~~~~~~~Allow Method
                if "private" not in http_method:
                    data[3]["Allow Method"] = http_method

        except:
            pass

        attack_vector.append(data)

    if form:
        for tag in form:
            try:
                action_page.append(tag.attrs['action'])
            except:
                action_page.append("None")
            try:
                action_type.append(tag.attrs['method'])
            except:
                action_type.append("None")

    return tag_list, tag_name_list, attack_vector, action_page, action_type


def corsCheck(req_res_packets):
    cors_check = "None"

    for packet in req_res_packets:
        resonse_header = packet["response"]["headers"]

        try:
            if resonse_header['access-control-allow-origin'] == "*":
                cors_check = "CORS Misconfiguration: *"
        except:
            pass

    return cors_check


# input tag 함수, Packets에서 불러오는 Cookie 값 + QueryString(Parameter) JSON 형태 예시 -> domain 테이블 Details 컬럼
"""
{
  "tag": [
    "tag A",
    "tag B"
  ],
  "cookie": {
    "PHPSESSID": "8a7s6f89sd6fg98f6s98d",
    "JSESSIONID": "abcdefghijklmnop"
  },
  "queryString": {
    "hello": "world"
  }
}

?hello=world
"""
