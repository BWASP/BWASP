import requests

class Config(object):
    def __init__(self):
        self.API_URL_PREFIX = "http://localhost:20102"

    def ret_API_URL_PREFIX(self):
        return self.API_URL_PREFIX


class Packets:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/packet"
        self.URL_PREFIX_Automation = {
            "GET": "/automation/index",
            "POST": "/automation"
        }
        self.URL_PREFIX_Manual = {
            "GET": "/manual/index",
            "POST": "/manual"
        }
        self.URL_PREFIX_Count = {
            "Automation": "/automation/count",
            "Manual": "/manual/count",
        }

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def GetAutomationCount(self):  # Automation count
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Count["Automation"],
            headers=self.requestHeaders
        )

        return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}

    def GetManualCount(self):  # Manual count
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Count["Manual"],
            headers=self.requestHeaders
        )
        """
        {
            "count": 3
        }
        """

        return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}

    def GetAutomationIndex(self):  # Automation index
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Automation["GET"],
            headers=self.requestHeaders
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}

    def GetManualIndex(self):  # Manual index
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Manual["GET"],
            headers=self.requestHeaders
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}

    def PostAutomation(self, data):  # Automation data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX + self.URL_PREFIX_Automation["POST"],
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}

    def PostManual(self, data):  # Manual data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX + self.URL_PREFIX_Manual["POST"],
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}


class Domain:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/domain"

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def PostDomain(self, data):  # Domain data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}


class CSPEvaluator:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/cspevaluator"

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def PostCSPEvaluator(self, data):  # CSPEvaluator data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}


class Job:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/job"

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def PostJob(self, data):  # job data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}


class SystemInfo:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/systeminfo"

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def PostSystemInfo(self, data):  # SystemInfo data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}

    def PATCHSystemInfo(self, data):  # SystemInfo data Update
        self.responseObj = self.requestObj.patch(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}


class Ports:
    def __init__(self):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + "/api/ports"

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def PostPorts(self, data):  # job data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.json()}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": "None"}
