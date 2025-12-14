FROM python:3.11-buster
ARG DEBIAN_FRONTEND=noninteractive

# Python 의존성 설치
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 작업 디렉토리 설정
WORKDIR /usr/src/app
COPY ./src/ .

# 환경변수 기본값
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV API_HOST=api
ENV API_PORT=3000
ENV PYTHONUNBUFFERED=1

# 워커 모드로 실행
CMD ["python3", "scouter.py"]
