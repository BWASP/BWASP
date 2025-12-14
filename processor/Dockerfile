FROM python:3.11-buster
ARG DEBIAN_FRONTEND=noninteractive

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/app
COPY ./src/ .

CMD ["python3", "scouter.py"]