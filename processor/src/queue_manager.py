"""
Redis Queue Manager
API/Client와 상호작용하는 큐 관리 모듈입니다.
스캔 작업을 큐에서 가져오고, 상태를 업데이트하며, 결과를 발행합니다.
"""
import redis
import json
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any, Callable

from config.settings import settings, JobStatus

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("QueueManager")


class RedisConnection:
    """Redis 연결 관리 싱글톤"""
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_connection(cls) -> redis.Redis:
        """Redis 연결 반환 (싱글톤)"""
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
                retry_on_timeout=True
            )
        return cls._instance
    
    @classmethod
    def close(cls):
        """Redis 연결 종료"""
        if cls._instance:
            cls._instance.close()
            cls._instance = None


class QueueManager:
    """Redis 큐 관리자"""
    
    def __init__(self):
        self.redis = RedisConnection.get_connection()
        self._running = False
    
    def is_connected(self) -> bool:
        """Redis 연결 상태 확인"""
        try:
            return self.redis.ping()
        except redis.ConnectionError:
            return False
    
    def wait_for_connection(self, max_retries: int = 30, retry_interval: int = 2) -> bool:
        """
        Redis 연결 대기
        
        Args:
            max_retries: 최대 재시도 횟수
            retry_interval: 재시도 간격 (초)
        
        Returns:
            연결 성공 여부
        """
        for attempt in range(max_retries):
            try:
                if self.redis.ping():
                    logger.info("Redis 연결 성공")
                    return True
            except redis.ConnectionError as e:
                logger.warning(f"Redis 연결 대기 중... ({attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
        
        logger.error("Redis 연결 실패")
        return False
    
    def enqueue_job(self, job_data: Dict[str, Any]) -> str:
        """
        작업을 큐에 추가
        
        Args:
            job_data: 작업 데이터 (url, depth, options 등)
        
        Returns:
            작업 ID
        """
        job_id = job_data.get("job_id", f"job_{int(time.time() * 1000)}")
        job_data["job_id"] = job_id
        job_data["created_at"] = datetime.now().isoformat()
        job_data["status"] = JobStatus.PENDING
        
        # 큐에 작업 추가
        self.redis.rpush(settings.QUEUE_SCAN_JOBS, json.dumps(job_data))
        
        # 작업 상태 저장
        self._update_job_status(job_id, JobStatus.PENDING, job_data)
        
        logger.info(f"작업 큐에 추가됨: {job_id}")
        return job_id
    
    def dequeue_job(self, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """
        큐에서 작업 가져오기 (블로킹)
        
        Args:
            timeout: 블로킹 타임아웃 (초), 0이면 무한 대기
        
        Returns:
            작업 데이터 또는 None
        """
        try:
            result = self.redis.blpop(settings.QUEUE_SCAN_JOBS, timeout=timeout)
            if result:
                _, job_json = result
                job_data = json.loads(job_json)
                logger.info(f"작업 수신: {job_data.get('job_id')}")
                return job_data
        except redis.ConnectionError as e:
            logger.error(f"Redis 연결 오류: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"작업 데이터 파싱 오류: {e}")
        
        return None
    
    def _update_job_status(self, job_id: str, status: str, data: Optional[Dict] = None):
        """작업 상태 업데이트 (내부용)"""
        status_key = f"{settings.KEY_JOB_STATUS}{job_id}"
        status_data = {
            "job_id": job_id,
            "status": status,
            "updated_at": datetime.now().isoformat()
        }
        if data:
            status_data["data"] = data
        
        # 상태 저장 (24시간 TTL)
        self.redis.setex(status_key, 86400, json.dumps(status_data))
        
        # Pub/Sub으로 상태 변경 알림
        self.redis.publish(settings.CHANNEL_JOB_STATUS, json.dumps(status_data))
    
    def update_job_running(self, job_id: str, message: str = ""):
        """작업 실행 중 상태로 업데이트"""
        self._update_job_status(job_id, JobStatus.RUNNING, {"message": message})
        logger.info(f"작업 실행 중: {job_id} - {message}")
    
    def update_job_progress(self, job_id: str, progress: int, message: str = ""):
        """작업 진행률 업데이트"""
        self._update_job_status(job_id, JobStatus.RUNNING, {
            "progress": progress,
            "message": message
        })
    
    def update_job_completed(self, job_id: str, result: Optional[Dict] = None):
        """작업 완료 상태로 업데이트"""
        self._update_job_status(job_id, JobStatus.COMPLETED, result)
        
        # 결과 저장
        if result:
            result_key = f"{settings.KEY_JOB_RESULT}{job_id}"
            self.redis.setex(result_key, 86400, json.dumps(result))
        
        logger.info(f"작업 완료: {job_id}")
    
    def update_job_failed(self, job_id: str, error: str):
        """작업 실패 상태로 업데이트"""
        self._update_job_status(job_id, JobStatus.FAILED, {"error": error})
        logger.error(f"작업 실패: {job_id} - {error}")
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """작업 상태 조회"""
        status_key = f"{settings.KEY_JOB_STATUS}{job_id}"
        status_json = self.redis.get(status_key)
        if status_json:
            return json.loads(status_json)
        return None
    
    def get_queue_length(self) -> int:
        """큐에 대기 중인 작업 수 반환"""
        return self.redis.llen(settings.QUEUE_SCAN_JOBS)
    
    def clear_queue(self):
        """큐 비우기 (주의: 모든 대기 작업 삭제)"""
        self.redis.delete(settings.QUEUE_SCAN_JOBS)
        logger.warning("큐가 비워졌습니다.")
    
    def start_worker(self, job_handler: Callable[[Dict[str, Any]], None]):
        """
        워커 시작 - 큐에서 작업을 가져와 처리
        
        Args:
            job_handler: 작업 처리 함수 (job_data를 받아 처리)
        """
        self._running = True
        logger.info("워커 시작됨 - 작업 대기 중...")
        
        while self._running:
            try:
                job_data = self.dequeue_job(timeout=5)
                
                if job_data is None:
                    continue
                
                job_id = job_data.get("job_id", "unknown")
                
                try:
                    self.update_job_running(job_id, "스캔 시작")
                    job_handler(job_data)
                    self.update_job_completed(job_id, {"message": "스캔 완료"})
                except Exception as e:
                    self.update_job_failed(job_id, str(e))
                    logger.exception(f"작업 처리 중 오류: {job_id}")
                    
            except KeyboardInterrupt:
                logger.info("워커 중지 요청됨")
                self.stop_worker()
            except Exception as e:
                logger.exception(f"워커 루프 오류: {e}")
                time.sleep(1)
    
    def stop_worker(self):
        """워커 중지"""
        self._running = False
        logger.info("워커 중지됨")


class JobPublisher:
    """
    작업 결과/이벤트 발행자
    API/Client에게 이벤트를 발행합니다.
    """
    
    def __init__(self):
        self.redis = RedisConnection.get_connection()
    
    def publish_event(self, channel: str, event_type: str, data: Dict[str, Any]):
        """이벤트 발행"""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.redis.publish(channel, json.dumps(event))
    
    def publish_scan_started(self, job_id: str, url: str):
        """스캔 시작 이벤트 발행"""
        self.publish_event(settings.CHANNEL_JOB_STATUS, "scan_started", {
            "job_id": job_id,
            "url": url
        })
    
    def publish_scan_progress(self, job_id: str, progress: int, current_url: str):
        """스캔 진행 이벤트 발행"""
        self.publish_event(settings.CHANNEL_JOB_STATUS, "scan_progress", {
            "job_id": job_id,
            "progress": progress,
            "current_url": current_url
        })
    
    def publish_scan_completed(self, job_id: str, summary: Dict[str, Any]):
        """스캔 완료 이벤트 발행"""
        self.publish_event(settings.CHANNEL_JOB_STATUS, "scan_completed", {
            "job_id": job_id,
            "summary": summary
        })
    
    def publish_scan_error(self, job_id: str, error: str):
        """스캔 오류 이벤트 발행"""
        self.publish_event(settings.CHANNEL_JOB_STATUS, "scan_error", {
            "job_id": job_id,
            "error": error
        })


# 전역 인스턴스
queue_manager = QueueManager()
job_publisher = JobPublisher()

