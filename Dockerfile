FROM python:3-alpine@sha256:78604a29496b7a1bd5ea5c985d69a0928db7ea32fcfbf71bbde3e317fdd9ac5e

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
