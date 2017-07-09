FROM python:2.7
ENV PYTHONUNBUFFERED 1

WORKDIR /api

RUN apt-get upgrade
RUN apt-get update -y

ADD . /api/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ./start.sh
