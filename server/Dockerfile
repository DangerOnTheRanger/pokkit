FROM debian:buster-slim

RUN apt-get update -y && apt-get install -y python3 python3-setuptools

ADD . /opt/pokkit-server
WORKDIR /opt/pokkit-server
RUN /opt/pokkit-server/setup.py install
CMD pokkit-server
