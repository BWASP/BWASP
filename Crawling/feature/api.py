import os, requests, datetime


class Packets:
    def GetAutomationIndex(self):  # Automation index
        pass

    def GetManualIndex(self):  # Manual index
        pass

    def PostAutomation(self, data):  # Automation data insert
        pass

    def PostManual(self, data):  # Manual data insert
        pass


class Domain:
    def PostDomain(self, data):  # Domain data insert
        pass


class CSPEvaluator:
    def PostCSPEvaluator(self, data):  # CSPEvaluator data insert
        pass


class Job:
    def PostJob(self, data):  # job data insert
        pass


class SystemInfo:
    def PostSystemInfo(self, data):  # SystemInfo data insert
        pass

    def PATCHSystemInfo(self, data):  # SystemInfo data Update
        pass


class Ports:
    def PostPorts(self, data):  # job data insert
        pass
