FROM python:3-alpine@sha256:bcca0a38a207b7b40c46e059e6ecf1ba3af833be665fb65ab8b7e81ac601e7d3

RUN ["apk","add","--no-cache","gcc","geos","libxml2-dev","libxslt-dev","musl-dev"]

WORKDIR /src
COPY requirements.txt /src/
RUN ["pip","install","--no-cache-dir","-r","/src/requirements.txt"]
COPY . /src/

ENTRYPOINT ["/src/placemark_linker/placemark_linker.py"]
