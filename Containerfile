FROM almalinux:9

ARG RUCIO_VERSION

RUN dnf -y update && dnf -y upgrade
RUN dnf -y install libcurl-devel gcc python3-devel openssl-devel
RUN dnf install -y python3-pip
RUN pip install pip setuptools wheel pycurl pyyaml rucio-clients==$RUCIO_VERSION
COPY rucio-ferry-sync.py /rucio-ferry-sync.py
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "/docker-entrypoint.sh" ]