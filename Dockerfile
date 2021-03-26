FROM python:3.8-slim-buster

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
RUN echo " " > /etc/apt/sources.list && echo "deb http://mirrors.aliyun.com/debian jessie main" >> /etc/apt/sources.list && echo "deb http://mirrors.aliyun.com/debian jessie-updates main" >> /etc/apt/sources.list && apt-get clean

RUN apt update && apt install libmediainfo-dev mediainfo libmediainfo-dev libmediainfo-doc gcc curl -y

RUN mkdir /pasteme

WORKDIR /pasteme

COPY requirements.txt /pasteme/
RUN cd /pasteme && pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
COPY . /pasteme
ENV PYTHONPATH=${PYTHONPATH}:/pasteme

EXPOSE 7332

CMD python3 pasteme/main.py