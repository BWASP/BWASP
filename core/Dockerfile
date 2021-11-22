FROM python:3.8-buster
ARG DEBIAN_FRONTEND=noninteractive

# Install requirements dependencies.
COPY ./requirements.txt /tmp/requirements.txt
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

# App directory
WORKDIR /usr/src/app
COPY src/. .
COPY dataset/attack_vector.json ./Crawling

# Install dependency - Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/goodle.list'
RUN apt-get update
RUN apt-get install -y google-chrome-stable

# RUN Python
CMD ["python3", "app.py"]