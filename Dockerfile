FROM ubuntu:18.04
MAINTAINER Atadjan && Luis

WORKDIR /vscan

COPY . /vscan/

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
# && pip install -r requirements.txt

EXPOSE 8080

CMD ["vscan"]
ENTRYPOINT []

