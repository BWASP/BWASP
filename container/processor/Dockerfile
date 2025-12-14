FROM python:3.11-buster
ARG DEBIAN_FRONTEND=noninteractive

# Chrome 및 필수 의존성 설치
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

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
