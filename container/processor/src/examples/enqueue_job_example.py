"""
API/Client에서 Processor 큐에 스캔 작업을 추가하는 예제

이 코드는 API 또는 Client 서비스에서 사용할 수 있습니다.
Redis를 통해 Processor에 스캔 작업을 요청합니다.
"""
import redis
import json
import uuid
from datetime import datetime


# Redis 설정 (환경변수에서 읽어오도록 수정 가능)
REDIS_HOST = "redis"  # Docker 환경에서는 "redis", 로컬에서는 "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 큐 이름 (processor의 settings.py와 동일해야 함)
QUEUE_SCAN_JOBS = "bwasp:queue:scan_jobs"
KEY_JOB_STATUS = "bwasp:job:status:"


class ScanJobClient:
    """스캔 작업 클라이언트 - API/Client에서 사용"""
    
    def __init__(self, redis_host=REDIS_HOST, redis_port=REDIS_PORT, redis_db=REDIS_DB):
        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            decode_responses=True
        )
    
    def submit_scan(self, url: str, depth: int = 1, options: dict = None) -> str:
        """
        스캔 작업 제출
        
        Args:
            url: 스캔할 URL
            depth: 크롤링 깊이 (기본값: 1)
            options: 스캔 옵션
        
        Returns:
            job_id: 작업 ID
        """
        if options is None:
            options = self._default_options()
        
        job_id = f"scan_{uuid.uuid4().hex[:12]}"
        
        job_data = {
            "job_id": job_id,
            "url": url,
            "depth": depth,
            "options": options,
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        # 큐에 작업 추가
        self.redis.rpush(QUEUE_SCAN_JOBS, json.dumps(job_data))
        
        # 작업 상태 저장
        status_key = f"{KEY_JOB_STATUS}{job_id}"
        self.redis.setex(status_key, 86400, json.dumps({
            "job_id": job_id,
            "status": "pending",
            "url": url,
            "created_at": job_data["created_at"]
        }))
        
        return job_id
    
    def get_job_status(self, job_id: str) -> dict:
        """작업 상태 조회"""
        status_key = f"{KEY_JOB_STATUS}{job_id}"
        status_json = self.redis.get(status_key)
        if status_json:
            return json.loads(status_json)
        return {"status": "not_found", "job_id": job_id}
    
    def get_queue_length(self) -> int:
        """대기 중인 작업 수"""
        return self.redis.llen(QUEUE_SCAN_JOBS)
    
    def _default_options(self) -> dict:
        """기본 스캔 옵션"""
        return {
            "Session": "",
            "API": {
                "google": {
                    "engineId": "",
                    "key": ""
                }
            },
            "tool": {
                "optionalJobs": []  # "portScan", "CSPEvaluate", "testPayloads"
            },
            "info": [],
            "maximumProcess": 5
        }


# 사용 예제
if __name__ == "__main__":
    # 클라이언트 생성
    client = ScanJobClient(redis_host="localhost")  # 로컬 테스트용
    
    # 스캔 작업 제출
    job_id = client.submit_scan(
        url="https://example.com",
        depth=2,
        options={
            "Session": "",
            "API": {"google": {"engineId": "", "key": ""}},
            "tool": {"optionalJobs": ["CSPEvaluate"]},
            "info": [],
            "maximumProcess": 5
        }
    )
    
    print(f"작업 제출됨: {job_id}")
    print(f"대기 중인 작업 수: {client.get_queue_length()}")
    
    # 작업 상태 확인
    status = client.get_job_status(job_id)
    print(f"작업 상태: {status}")

