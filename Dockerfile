FROM python:3-alpine@sha256:c7eb5c92b7933fe52f224a91a1ced27b91840ac9c69c58bef40d602156bcdb41

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
