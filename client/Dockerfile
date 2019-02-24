FROM debian:sid-slim
WORKDIR /pokkit
# preinstall grpc so pip doesn't attempt to install it from source
RUN apt-get update -y
RUN apt-get install -y python3-grpcio
# install FUSE
RUN apt-get install -y fuse python3-fuse
# install distutils
RUN apt-get install -y python3-setuptools

# copy over entrypoint
COPY docker-entrypoint.sh /pokkit/docker-entrypoint.sh
# copy over build support files
COPY setup.py /pokkit/setup.py
# copy over pokkit client source and install
COPY pokkit /pokkit/pokkit
RUN python3 setup.py install
ENTRYPOINT /pokkit/docker-entrypoint.sh