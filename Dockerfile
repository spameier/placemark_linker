FROM python:3-alpine@sha256:804ad02b9ba67ea1f8307eeb6407b121c6bd6bb19d3f182aae166821eb59d6a4

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
