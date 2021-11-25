FROM python:3.8-buster
ARG DEBIAN_FRONTEND=noninteractive

ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ./src/docker-entrypoint.sh /tmp/docker-entrypoint.sh
COPY ./requirements.txt /tmp/requirements.txt

RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# App directory
WORKDIR /usr/src/app
COPY src/. .

# RUN Python
# CMD ["python3", "app.py"]

RUN ["chmod", "+x", "/tmp/docker-entrypoint.sh"]
ENTRYPOINT ["sh","/tmp/docker-entrypoint.sh"]
