FROM python:3-alpine@sha256:5dad625efcbc6fad19c10b7b2bfefa1c7a8129c8f8343106b639c27dd9e7db2c

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
