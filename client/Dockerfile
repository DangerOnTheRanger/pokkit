FROM debian:sid-slim

# preinstall python packages so setup.py doesn't attempt to install it from source
RUN apt-get update -y
RUN apt-get install -y python3-grpcio  python3-setuptools python3-pip python3-setuptools python3-fuse python3-yaml
# TODO: install python3-pyqt5 and remove python3-pip, but for some
# reason even with python3-pyqt5 setuptools tries to install pyqt5.

RUN pip3 install PyQt5

# copy over entrypoint
COPY docker-entrypoint.sh /pokkit/docker-entrypoint.sh

# copy over build support files
COPY setup.py /pokkit/setup.py

# copy over pokkit client source and install
COPY pokkit /pokkit/pokkit
WORKDIR /pokkit
RUN python3 setup.py install
ENTRYPOINT /pokkit/docker-entrypoint.sh
