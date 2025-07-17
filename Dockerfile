FROM python:3-alpine@sha256:37b14db89f587f9eaa890e4a442a3fe55db452b69cca1403cc730bd0fbdc8aaf

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
