FROM debian:sid-slim
WORKDIR /pokkit
# preinstall grpc so pip doesn't attempt to install it from source
RUN apt-get update -y
RUN apt-get install -y python3-grpcio
# install distutils
RUN apt-get install -y python3-setuptools
# copy over build support files
COPY setup.py /pokkit/setup.py
COPY build-scripts /pokkit/build-scripts
# copy over pokkit client source
COPY lib /pokkit/lib
RUN python3 setup.py install