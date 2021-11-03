import os, requests, datetime


class Packets:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/packet"
        self.URL_PREFIX_Automation = {
            "GET": "/automation/index",
            "POST": "/automation"
        }
        self.URL_PREFIX_Manual = {
            "GET": "/manual/index",
            "POST": "/manual"
        }

        self.requestObj = requests
        self.responseObj = ""
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def GetAutomationIndex(self):  # Automation index
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Automation["GET"],
            headers=self.requestHeaders
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}

    def GetManualIndex(self):  # Manual index
        self.responseObj = self.requestObj.get(
            url=self.URL_PREFIX + self.URL_PREFIX_Manual["GET"],
            headers=self.requestHeaders
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}

    def PostAutomation(self, data):  # Automation data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX + self.URL_PREFIX_Automation["POST"],
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}

    def PostManual(self, data):  # Manual data insert
        self.responseObj = self.requestObj.post(
            url=self.URL_PREFIX + self.URL_PREFIX_Manual["POST"],
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 201:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}


class Domain:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/domain"

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
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}


class CSPEvaluator:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/cspevaluator"

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
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}


class Job:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/job"

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
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}


class SystemInfo:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/systeminfo"

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
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}

    def PATCHSystemInfo(self, data):  # SystemInfo data Update
        self.responseObj = self.requestObj.patch(
            url=self.URL_PREFIX,
            headers=self.requestHeaders,
            data=data
        )

        if self.responseObj.status_code == 200:
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}


class Ports:
    def __init__(self):
        self.URL_PREFIX = "http://localhost:20102/api/ports"

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
            return {"status": self.responseObj.status_code, "message": "Success", "retData": self.responseObj.text}
        else:
            return {"status": self.responseObj.status_code, "message": "Failed", "retData": self.responseObj.text}

