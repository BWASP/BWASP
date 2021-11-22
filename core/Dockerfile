FROM python:3.8-buster
ARG DEBIAN_FRONTEND=noninteractive

# Install requirements dependencies.
COPY ./requirements.txt /tmp/requirements.txt
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# App directory
WORKDIR /usr/src/app
COPY src/. .
COPY dataset/attack_vector.json ./Crawling

# RUN Python
CMD ["python3", "app.py"]