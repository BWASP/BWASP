"""
BWASP Processor - Scouter
웹 애플리케이션 보안 스캐너 엔진

Redis 큐에서 작업을 받아 처리하는 워커 모드로 동작합니다.
"""
from seleniumwire import webdriver
from multiprocessing import Process, Manager
from urllib.parse import urlparse, urljoin
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import json
import logging
import time

import analyst
from feature.packet_capture import PacketCapture
from feature.get_res_links import GetReslinks
from feature.csp_evaluator import cspAnalysis
from feature.get_ports import GetPort
from feature.get_page_links import GetPageLinks
from feature import get_cookies, db, func
from feature.api import *
from attack_vector import attackHeader, robotsTxt, errorPage, directoryIndexing, adminPage
from queue_manager import queue_manager, job_publisher, QueueManager
from config.settings import settings, JobStatus

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Scouter")


class ScanContext:
    """스캔 컨텍스트 - 스캔 세션 상태 관리"""
    
    def __init__(self, job_id: str = None):
        self.job_id = job_id
        self.check = True
        self.input_url = ""
        self.visited_links = []
        self.count_links = {}
        self.previous_packet_count = 0
        
        # 분석 데이터
        self.http_method = None
        self.infor_vector = None
        self.robots_result = False
        self.error_result = False
        self.directory_indexing = []
        self.admin_page = []
        self.testPayloads = False
        
        # 프로세스 관리
        self.load_packet_indexes = []
        self.process_list = []
        self.detect_list = None
        self.lock = None
    
    def get_analysis_data(self):
        """분석 데이터 딕셔너리 반환"""
        return {
            "http_method": self.http_method,
            "infor_vector": self.infor_vector,
            "robots_result": self.robots_result,
            "error_result": self.error_result,
            "directory_indexing": self.directory_indexing,
            "admin_page": self.admin_page,
            "testPayloads": self.testPayloads
        }


class Scanner:
    """웹 스캐너 클래스"""
    
    def __init__(self):
        self.driver = None
        self.ctx = None
    
    def scan(self, url: str, depth: int, options: dict, job_id: str = None):
        """
        스캔 실행
        
        Args:
            url: 대상 URL
            depth: 크롤링 깊이
            options: 스캔 옵션
            job_id: 작업 ID (큐에서 받은 경우)
        """
        self.ctx = ScanContext(job_id)
        
        manager = Manager()
        self.ctx.detect_list = manager.list()
        self.ctx.detect_list.append({})
        self.ctx.lock = manager.Lock()
        
        try:
            self.driver = self._init_selenium()
            
            if job_id:
                job_publisher.publish_scan_started(job_id, url)
            
            self._visit(url, depth, options)
            
            # 모든 프로세스 대기
            for each_process in self.ctx.process_list:
                each_process.join()
            
            if job_id:
                job_publisher.publish_scan_completed(job_id, {
                    "visited_pages": len(self.ctx.visited_links),
                    "packets_captured": self.ctx.previous_packet_count
                })
                
        except Exception as e:
            logger.exception(f"스캔 중 오류 발생: {e}")
            if job_id:
                job_publisher.publish_scan_error(job_id, str(e))
            raise
        finally:
            if self.driver:
                self.driver.quit()
    
    def _init_selenium(self):
        """Selenium WebDriver 초기화"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("lang=ko_KR")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option("prefs", {
            "download_restrictions": 3
        })
        
        seleniumwire_options = {
            "disable_encoding": True,
            'request_storage': 'memory'
        }
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service,
            seleniumwire_options=seleniumwire_options,
            options=chrome_options
        )
        
        return driver
    
    def _visit(self, url: str, depth: int, options: dict):
        """페이지 방문 및 분석"""
        try:
            self.driver.get(url)
            
            # 세션 쿠키 설정
            if "=" in options.get("Session", ""):
                for each_session in options["Session"].split(";"):
                    split_point = each_session.index("=")
                    if split_point:
                        self.driver.add_cookie({
                            'name': each_session[0:split_point].lstrip(),
                            'value': each_session[split_point+1:]
                        })
            self.driver.refresh()
            
            try:
                alert = self.driver.switch_to_alert()
                alert.accept()
            except:
                pass
                
        except Exception as e:
            logger.warning(f"페이지 접근 오류: {e}")
        
        # 최초 방문 시 초기화
        if self.ctx.check:
            self._initialize_scan(options)
        
        # 패킷 캡처
        packet_obj = PacketCapture()
        packet_obj.start(self.driver)
        
        cur_page_links = []
        
        # Open Redirect 검증
        if self._is_open_redirection(url, self.driver.current_url, self.ctx.input_url):
            packet_obj.filterPath(url)
            packet_obj.packets[0]["open_redirect"] = True
        else:
            cur_page_links = self._extract_page_links(packet_obj)
        
        # 쿠키 분석
        cookie_result = get_cookies.start(self.driver.current_url, packet_obj.packets)
        
        # 패킷 저장
        packet_obj.deleteUselessBody()
        db.insertPackets(packet_obj.packets)
        
        # 비동기 분석 프로세스 시작
        p = Process(
            target=self._analysis_worker,
            args=(
                self.ctx.input_url,
                packet_obj.packets,
                cur_page_links,
                options,
                cookie_result,
                self.ctx.detect_list,
                self.ctx.lock,
                self.driver.current_url,
                self.ctx.previous_packet_count,
                self.ctx.get_analysis_data()
            )
        )
        self.ctx.previous_packet_count += len(packet_obj.packets)
        p.start()
        self.ctx.process_list.append(p)
        
        # 프로세스 수 관리
        if options.get('maximumProcess', 0) > 0:
            if len(self.ctx.process_list) > options['maximumProcess']:
                for process in self.ctx.process_list:
                    process.join()
                self.ctx.process_list = []
        
        # 깊이 체크
        if depth == 0:
            return
        
        # 하위 링크 방문
        for visit_url in cur_page_links:
            if visit_url in self.ctx.visited_links:
                continue
            if not func.isSameDomain(self.ctx.input_url, visit_url):
                continue
            if func.isSamePath(visit_url, self.ctx.visited_links):
                continue
            if func.isExistExtension(visit_url, ["image"]):
                continue
            if self._check_count_link(visit_url):
                continue
            
            self.ctx.visited_links.append(visit_url)
            
            # 진행 상황 발행
            if self.ctx.job_id:
                progress = min(90, int(len(self.ctx.visited_links) / max(len(cur_page_links), 1) * 100))
                job_publisher.publish_scan_progress(self.ctx.job_id, progress, visit_url)
            
            self._visit(visit_url, depth - 1, options)
    
    def _initialize_scan(self, options: dict):
        """스캔 초기화 (최초 방문 시)"""
        google_api = options.get("API", {}).get("google", {})
        session = options.get("Session", "")
        
        self.ctx.directory_indexing = directoryIndexing(self.driver.current_url, google_api)
        self.ctx.admin_page = adminPage(self.driver.current_url, google_api)
        self.ctx.http_method, self.ctx.infor_vector = attackHeader(self.driver.current_url, session)
        self.ctx.robots_result = robotsTxt(self.driver.current_url)
        self.ctx.error_result = errorPage(self.driver.current_url)
        
        db.postWebInfo(self.driver.current_url)
        
        self.ctx.input_url = self.driver.current_url
        self.ctx.visited_links.append(self.ctx.input_url)
        self.ctx.check = False
        
        # 포트 스캔
        if "portScan" in options.get("tool", {}).get("optionalJobs", []):
            target_port = GetPort().getPortsOffline(self.ctx.input_url)
            db.insertPorts(target_port, self.ctx.input_url)
        else:
            target_port, cloud_info = GetPort().getPortsOnline(self.ctx.input_url)
            self.ctx.detect_list[0] = cloud_info
            db.insertPorts(target_port, self.ctx.input_url)
        
        # CSP 평가
        if "CSPEvaluate" in options.get("tool", {}).get("optionalJobs", []):
            csp_result = cspAnalysis().start(self.driver.current_url)
            db.insertCSP(csp_result)
        
        # 페이로드 테스트
        if "testPayloads" in options.get("tool", {}).get("optionalJobs", []):
            self.ctx.testPayloads = True
    
    def _extract_page_links(self, packet_obj: PacketCapture) -> list:
        """페이지에서 링크 추출"""
        cur_page_links = []
        count = 0
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        packet_tmp = packet_obj.packets
        
        while True:
            cur_page_links += GetPageLinks(self.driver.current_url, self.driver.page_source).start()
            cur_page_links += GetReslinks(self.driver.current_url, packet_tmp, self.driver.page_source).start()
            
            if count == len(iframes):
                break
            
            self.driver.switch_to_default_content()
            self.driver.switch_to_frame(iframes[count])
            count += 1
            packet_tmp = []
        
        return list(set(packet_obj.deleteFragment(cur_page_links)))
    
    def _check_count_link(self, visit_url: str) -> bool:
        """링크 방문 횟수 체크"""
        visit_path = urlparse(visit_url).path
        tmp_path = visit_path.split("/")
        
        for path in tmp_path[::-1]:
            if path.isnumeric():
                tmp_path.pop()
        
        visit_path = "/".join(tmp_path)
        
        try:
            if self.ctx.count_links[visit_path]["count"] > 5:
                return True
            self.ctx.count_links[visit_path]["count"] += 1
        except:
            self.ctx.count_links[visit_path] = {"count": 1}
        
        return False
    
    def _is_open_redirection(self, visit_url: str, current_url: str, target_url: str) -> bool:
        """Open Redirect 취약점 검사"""
        url = urlparse(visit_url)
        if url.query:
            url_query = url.query.split("&")
            
            if not func.isSameDomain(current_url, target_url) or not func.isSamePath(visit_url, current_url):
                pattern_url = re.compile(
                    r"((?:http|ftp|https)(?://)([\w_-]+((\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)"
                )
                
                for query in url_query:
                    value = query.split("=")
                    if len(value) == 1:
                        continue
                    
                    value = value[1]
                    if pattern_url.findall(value):
                        return True
                    if urljoin(target_url, value) == current_url:
                        return True
        return False
    
    @staticmethod
    def _analysis_worker(input_url, req_res_packets, cur_page_links, options, cookie_result,
                         detect_list, lock, current_url, previous_packet_count, analysis_data):
        """분석 워커 (별도 프로세스에서 실행)"""
        load_packet_indexes = []
        recent_packet_count = len(req_res_packets) + previous_packet_count
        
        if len(load_packet_indexes) < recent_packet_count:
            # API 응답에서 패킷 인덱스 목록 가져오기
            api_response = Packets().GetAutomationIndex()
            if api_response["status"] == 200 and api_response["retData"]:
                # retData가 {"id": [...]} 형태
                load_packet_indexes = api_response["retData"].get("id", [])
            else:
                logger.warning(f"패킷 인덱스 조회 실패: {api_response}")
                load_packet_indexes = []
        
        packet_indexes = load_packet_indexes[previous_packet_count:recent_packet_count]
        
        analyst.start(
            detect_list, lock, input_url, req_res_packets, cur_page_links,
            current_url, packet_indexes, options.get('info', [])
        )
        
        db.insertDomains(
            req_res_packets, cookie_result, packet_indexes,
            input_url, analysis_data, options.get("Session", "")
        )
        db.updateWebInfo(detect_list[0])


def process_job(job_data: dict):
    """
    큐에서 받은 작업 처리
    
    Args:
        job_data: 작업 데이터
            - job_id: 작업 ID
            - url: 대상 URL
            - depth: 크롤링 깊이
            - options: 스캔 옵션
    """
    job_id = job_data.get("job_id")
    url = job_data.get("url")
    depth = job_data.get("depth", 1)
    options = job_data.get("options", {})
    
    logger.info(f"작업 처리 시작: {job_id} - {url}")
    
    scanner = Scanner()
    scanner.scan(url, depth, options, job_id)
    
    logger.info(f"작업 처리 완료: {job_id}")


def run_worker():
    """Redis 큐 워커 실행"""
    logger.info("BWASP Processor 워커 시작")
    logger.info(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    
    # Redis 연결 대기
    if not queue_manager.wait_for_connection():
        logger.error("Redis 연결 실패로 종료")
        return
    
    logger.info("작업 대기 중...")
    queue_manager.start_worker(process_job)


def run_standalone(url: str, depth: int, options: dict):
    """
    독립 실행 모드 (레거시 지원)
    
    Args:
        url: 대상 URL
        depth: 크롤링 깊이
        options: 스캔 옵션
    """
    logger.info(f"독립 실행 모드: {url}")
    scanner = Scanner()
    scanner.scan(url, depth, options)


# =====================================================
# 레거시 API 지원 (하위 호환성)
# =====================================================

# 전역 변수 (레거시)
START_OPTIONS = None
ANALYSIS_DATA = None
LOAD_PACKET_INDEXES = None
PROCESS_LIST = None
DETECT_LIST = None
LOCK = None


def initGlobal():
    """레거시: 전역 변수 초기화"""
    global START_OPTIONS, ANALYSIS_DATA, LOAD_PACKET_INDEXES
    global PROCESS_LIST, DETECT_LIST, LOCK
    
    START_OPTIONS = {
        "check": True,
        "input_url": "",
        "visited_links": [],
        "count_links": {},
        "previous_packet_count": 0
    }
    
    ANALYSIS_DATA = {
        "http_method": None,
        "infor_vector": None,
        "robots_result": False,
        "error_result": False,
        "directory_indexing": [],
        "admin_page": [],
        "testPayloads": False
    }
    
    LOAD_PACKET_INDEXES = []
    PROCESS_LIST = []
    DETECT_LIST = []
    LOCK = None


def start(url, depth, options):
    """레거시: 스캔 시작 함수"""
    run_standalone(url, depth, options)


# =====================================================
# 메인 엔트리포인트
# =====================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--standalone":
        # 독립 실행 모드 (테스트용)
        if len(sys.argv) < 3:
            print("Usage: python scouter.py --standalone <url> [depth]")
            sys.exit(1)
        
        test_url = sys.argv[2]
        test_depth = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        test_options = {
            "Session": "",
            "API": {"google": {"engineId": "", "key": ""}},
            "tool": {"optionalJobs": []},
            "info": [],
            "maximumProcess": 5
        }
        
        run_standalone(test_url, test_depth, test_options)
    else:
        # 기본: 워커 모드
        run_worker()
