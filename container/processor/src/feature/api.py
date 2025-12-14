"""
BWASP Processor - API Client
API 서버와 통신하는 클라이언트 모듈
Docker 환경에서는 api:3000, 로컬에서는 localhost:20102 사용
"""
import os
import requests
import datetime
import logging
from typing import Optional, Dict, Any, List, Union

# 로깅 설정
logger = logging.getLogger("API")


class Config(object):
    """API 설정 클래스 - 환경변수 지원"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_config()
        return cls._instance
    
    def _init_config(self):
        # Docker 환경: api:3000, 로컬: localhost:20102
        api_host = os.getenv("API_HOST", "api")
        api_port = os.getenv("API_PORT", "3000")
        self.API_URL_PREFIX = f"http://{api_host}:{api_port}"
        logger.info(f"API URL: {self.API_URL_PREFIX}")

    def ret_API_URL_PREFIX(self):
        return self.API_URL_PREFIX


class BaseAPIClient:
    """API 클라이언트 기본 클래스"""
    
    def __init__(self, endpoint: str):
        self.URL_PREFIX = Config().ret_API_URL_PREFIX() + endpoint
        self.requestObj = requests
        self.requestHeaders = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        self.timeout = 30  # 요청 타임아웃 (초)
    
    def _request(self, method: str, url: str, data: Any = None) -> Dict[str, Any]:
        """HTTP 요청을 보내고 응답을 처리"""
        try:
            if method == "GET":
                response = self.requestObj.get(
                    url=url,
                    headers=self.requestHeaders,
                    timeout=self.timeout
                )
            elif method == "POST":
                response = self.requestObj.post(
                    url=url,
                    headers=self.requestHeaders,
                    data=data,
                    timeout=self.timeout
                )
            elif method == "PATCH":
                response = self.requestObj.patch(
                    url=url,
                    headers=self.requestHeaders,
                    data=data,
                    timeout=self.timeout
                )
            else:
                return {"status": 400, "message": "Unsupported method", "retData": None}
            
            # 응답 처리
            if response.status_code in [200, 201]:
                json_data = response.json()
                # API 응답이 { data: ... } 형식이면 data 필드 추출
                if isinstance(json_data, dict) and "data" in json_data:
                    return {
                        "status": response.status_code,
                        "message": "Success",
                        "retData": json_data["data"]
                    }
                return {
                    "status": response.status_code,
                    "message": "Success",
                    "retData": json_data
                }
            else:
                logger.warning(f"API request failed: {url} - {response.status_code}")
                return {
                    "status": response.status_code,
                    "message": "Failed",
                    "retData": None
                }
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout: {url}")
            return {"status": 408, "message": "Timeout", "retData": None}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"API connection error: {url} - {e}")
            return {"status": 503, "message": "Connection Error", "retData": None}
        except Exception as e:
            logger.error(f"API request error: {url} - {e}")
            return {"status": 500, "message": str(e), "retData": None}


class Packets(BaseAPIClient):
    """패킷 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/packet")
    
    def GetAutomationIndex(self) -> Dict[str, Any]:
        """자동화 패킷 ID 목록 조회"""
        result = self._request("GET", f"{self.URL_PREFIX}/automation/index")
        # ID 목록을 반환 (API가 [1, 2, 3, ...] 형태로 반환)
        if result["status"] == 200 and result["retData"] is not None:
            # retData가 리스트면 그대로, 아니면 id 키로 감싸서 반환
            ids = result["retData"]
            if isinstance(ids, list):
                result["retData"] = {"id": ids}
            else:
                result["retData"] = {"id": ids if ids else []}
        return result
    
    def GetManualIndex(self) -> Dict[str, Any]:
        """수동 패킷 ID 목록 조회"""
        result = self._request("GET", f"{self.URL_PREFIX}/manual/index")
        if result["status"] == 200 and result["retData"] is not None:
            ids = result["retData"]
            if isinstance(ids, list):
                result["retData"] = {"id": ids}
            else:
                result["retData"] = {"id": ids if ids else []}
        return result
    
    def PostAutomation(self, data: str) -> Dict[str, Any]:
        """자동화 패킷 생성"""
        return self._request("POST", f"{self.URL_PREFIX}/automation", data)
    
    def PostManual(self, data: str) -> Dict[str, Any]:
        """수동 패킷 생성"""
        return self._request("POST", f"{self.URL_PREFIX}/manual", data)


class Domain(BaseAPIClient):
    """도메인 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/domain")
    
    def PostDomain(self, data: str) -> Dict[str, Any]:
        """도메인 데이터 생성"""
        return self._request("POST", self.URL_PREFIX, data)
    
    def GetDomains(self) -> Dict[str, Any]:
        """모든 도메인 조회"""
        return self._request("GET", self.URL_PREFIX)


class CSPEvaluator(BaseAPIClient):
    """CSP 평가 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/cspevaluator")
    
    def PostCSPEvaluator(self, data: str) -> Dict[str, Any]:
        """CSP 평가 데이터 생성"""
        return self._request("POST", self.URL_PREFIX, data)


class Job(BaseAPIClient):
    """작업 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/job")
    
    def PostJob(self, data: str) -> Dict[str, Any]:
        """작업 생성"""
        return self._request("POST", self.URL_PREFIX, data)
    
    def GetJobs(self) -> Dict[str, Any]:
        """모든 작업 조회"""
        return self._request("GET", self.URL_PREFIX)


class SystemInfo(BaseAPIClient):
    """시스템 정보 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/systeminfo")
    
    def PostSystemInfo(self, data: str) -> Dict[str, Any]:
        """시스템 정보 생성"""
        return self._request("POST", self.URL_PREFIX, data)
    
    def PATCHSystemInfo(self, data: str) -> Dict[str, Any]:
        """시스템 정보 수정"""
        return self._request("PATCH", self.URL_PREFIX, data)
    
    def GetSystemInfo(self) -> Dict[str, Any]:
        """시스템 정보 조회"""
        return self._request("GET", self.URL_PREFIX)


class Ports(BaseAPIClient):
    """포트 스캔 API 클라이언트"""
    
    def __init__(self):
        super().__init__("/api/ports")
    
    def PostPorts(self, data: str) -> Dict[str, Any]:
        """포트 스캔 결과 생성"""
        return self._request("POST", self.URL_PREFIX, data)
    
    def GetPorts(self) -> Dict[str, Any]:
        """포트 스캔 결과 조회"""
        return self._request("GET", self.URL_PREFIX)
