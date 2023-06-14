FROM python:3.8.9

USER root
COPY ./requirements.txt /usr/src/requirements.txt

USER root
RUN /usr/local/bin/python -m pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/

USER root
RUN pip install --user -r /usr/src/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /usr/src/blog
