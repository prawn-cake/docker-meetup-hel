FROM python:3.5

MAINTAINER Maksim Ekimovskii<maksim.ekimovskii@zalando.fi>

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt