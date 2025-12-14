import requests

class cspAnalysis:
    def __init__(self):
        self.third_data = dict()

    def cspAnalyst(self):
        if self.second_data[0] == '':  # 빈 공백이 key에 포함된 경우가 있어서 별도 정리
            del (self.second_data[0])
            if len(self.second_data) > 2:  # 제거 후에도 value가 2개 이상인 경우 파악
                self.third_data[self.second_data[0]] = self.second_data
            else:
                self.third_data[self.second_data[0]] = self.second_data[1]
        else:
            tmp = self.second_data[0]
            del (self.second_data[0])
            self.third_data[tmp] = self.second_data

    def start(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        r = requests.get(url, headers=headers, verify=False)

        try:
            if r.headers['content-security-policy']:
                first_data = r.headers['content-security-policy'].split(';')
                length = len(r.headers['content-security-policy'].split(';'))
                for i in range(0, length):
                    self.second_data = first_data[i].split(' ')
                    if len(self.second_data) > 2: #value가 2개 이상인 경우 파악
                        self.cspAnalyst()
                    elif len(self.second_data) == 3:
                        self.third_data[self.second_data[1]] = self.second_data[2]
                    else:
                        self.third_data[self.second_data[0]] = self.second_data[1]
        except:
            pass

        return self.third_data

'''
if __name__ == "__main__":
    url = "https://github.com/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    start(url)
'''