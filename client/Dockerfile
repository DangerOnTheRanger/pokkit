FROM debian:sid-slim

# preinstall grpc so pip doesn't attempt to install it from source
RUN apt-get update -y
RUN apt-get install -y python3-grpcio  python3-setuptools python3-pip
# TODO: install python3-pyqt5 and remove python3-pip, but for some
# reason even with python3-pyqt5 setuptools tries to install pyqt5.

# copy over build support files
COPY setup.py /pokkit/setup.py

# copy over pokkit client source and install
COPY pokkit /pokkit/pokkit
WORKDIR /pokkit
RUN python3 setup.py install

ENTRYPOINT /usr/local/bin/pokkit
