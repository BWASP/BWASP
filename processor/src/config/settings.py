"""
Processor Configuration Settings
환경변수를 통해 Redis, API 등의 설정을 관리합니다.
"""
import os


class Settings:
    """애플리케이션 설정"""
    
    # Redis 설정
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    
    # 큐 이름
    QUEUE_SCAN_JOBS = "bwasp:queue:scan_jobs"          # 스캔 작업 큐
    QUEUE_SCAN_RESULTS = "bwasp:queue:scan_results"    # 스캔 결과 큐
    
    # 채널 (Pub/Sub)
    CHANNEL_JOB_STATUS = "bwasp:channel:job_status"    # 작업 상태 알림 채널
    
    # 작업 상태 키 프리픽스
    KEY_JOB_STATUS = "bwasp:job:status:"               # 작업 상태 저장 키
    KEY_JOB_RESULT = "bwasp:job:result:"               # 작업 결과 저장 키
    
    # API 설정
    API_HOST = os.getenv("API_HOST", "api")
    API_PORT = int(os.getenv("API_PORT", 3000))
    
    @classmethod
    def get_api_url(cls):
        """API URL 반환"""
        return f"http://{cls.API_HOST}:{cls.API_PORT}"
    
    @classmethod
    def get_redis_url(cls):
        """Redis URL 반환"""
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"


# 작업 상태 정의
class JobStatus:
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


settings = Settings()

