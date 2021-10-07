import requests

third_data = {}

def cspAnalyst(second_data):
    if second_data[0] == '':  # 빈 공백이 key에 포함된 경우가 있어서 별도 정리
        del (second_data[0])
        if len(second_data) > 2:  # 제거 후에도 value가 2개 이상인 경우 파악
            third_data[second_data[0]] = second_data
        else:
            third_data[second_data[0]] = second_data[1]
    else:
        tmp = second_data[0]
        del (second_data[0])
        third_data[tmp] = second_data

def cspHeader(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    #third_data = {}

    try:
        if r.headers['content-security-policy']:
            first_data = r.headers['content-security-policy'].split(';')
            length = len(r.headers['content-security-policy'].split(';'))
            for i in range(0, length):
                second_data = first_data[i].split(' ')
                if len(second_data) > 2: #value가 2개 이상인 경우 파악
                    cspAnalyst(second_data)
                elif len(second_data) == 3:
                    third_data[second_data[1]] = second_data[2]
                else:
                    third_data[second_data[0]] = second_data[1]
    except:
        pass

    return third_data

if __name__ == "__main__":
    url = "https://github.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    cspHeader(url)