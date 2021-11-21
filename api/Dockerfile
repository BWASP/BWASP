FROM python:3.8-buster
ARG DEBIAN_FRONTEND=noninteractive


COPY ./requirements.txt /tmp/requirements.txt
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# App directory
WORKDIR /usr/src/app
COPY src/. .

# RUN Python
CMD ["python3", "app.py"]