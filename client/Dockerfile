FROM debian:sid-slim

# preinstall python packages so setup.py doesn't attempt to install it from source
RUN apt-get update -y
RUN apt-get install -y \
	python3-grpcio \
	python3-setuptools \
	python3-pip \
	python3-fusepy \
	python3-yaml \
	python3-requests \
	libgl1-mesa-glx

# this eliminates the need to install it late ron
RUN pip3 install PyQt5
# TODO: install python3-pyqt5 and remove python3-pip, but for some
# reason even with python3-pyqt5 setuptools tries to install pyqt5.

# copy over pokkit client source and install
COPY . /pokkit
WORKDIR /pokkit
RUN python3 setup.py install
ENTRYPOINT /pokkit/docker-entrypoint.sh
