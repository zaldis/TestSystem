FROM python:3.7-buster

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache

RUN mkdir -p /opt/app/myquestions
RUN mkdir -p /opt/app/core

COPY myquestions/ /opt/app/myquestions/
COPY core/ /opt/app/core/
COPY manage.py requirements.txt /opt/app/

WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
