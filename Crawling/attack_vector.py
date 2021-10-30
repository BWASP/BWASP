from bs4 import BeautifulSoup
import requests


def attack_header(target_url):
    r = requests.get(target_url)
    dict_data = r.headers
    infor_data = ""
    infor_vector = ""
    http_method = requests.options(target_url)
    try:
        http_method = http_method.headers['Allow']
    except:
        http_method = "http method private data :("

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



def input_tag(response_body):
    # form tag action and input tag and input name parse
    soup = BeautifulSoup(response_body, 'html.parser')
    tag_list=[]
    tag_name_list=[]
    board = ""
    login = ""
    try:
        text = soup.find_all('input')
        text_length = len(text)
    except:
        text_length = 0

    try:
        form = soup.find_all('form')
    except:
        form = "none"

    for tag in text:

        try:
            tag.attrs['type']

            if tag.attrs['type'] != "submit" and text_length != 0:
                tag_list.append(tag)  # input tag 값 ex) <input ~
                try:
                    tag_name_list.append(tag.attrs['name'])  # parameter name 값 ex) uname
                except:
                    print("name option No: " + str(tag))

                # th tag check (board) and type="password" check (login)
                if "<th" in response_body:
                    board = "board check (sql injection and xss)"

                if tag.attrs['type'] == "password":
                    login = "login check (sql injection)"

        except:
            pass

    if form != "none":
        for tag in form:
            print(tag.attrs['action'])

    return tag_list, tag_name_list, board, login

