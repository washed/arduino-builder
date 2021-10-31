FROM python:3.9-slim-buster

RUN apt-get clean && apt-get update && apt-get upgrade -y
RUN apt-get install curl clang-format sudo -y
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/0.19.3/install.sh | BINDIR=/usr/bin sh

WORKDIR /root

COPY arduino-cli-config.py /root/arduino-cli-config.py

ENTRYPOINT [ "python", "arduino-cli-config.py" ]
