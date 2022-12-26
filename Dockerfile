FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get -qqy update
RUN apt-get -qqy --no-install-recommends install locales apt-utils

RUN apt-get -qqy install python3-pip

ADD ./ /app/
WORKDIR /app/

RUN pip install -r requirements.txt

ENV fastapi_host=0.0.0.0
ENV fastapi_port=8080
ENV postgress_host=172.19.0.2
ENV postgress_password=password
ENV postgress_user=postgres
ENV postgress_db=test

ENTRYPOINT ["python3", "main.py"]