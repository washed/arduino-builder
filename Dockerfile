FROM python:3.9-slim-buster

RUN apt-get clean && apt-get update && apt-get upgrade -y
RUN apt-get install curl clang-format sudo -y
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/0.19.3/install.sh | BINDIR=/usr/bin sh

WORKDIR /usr/src/app

RUN python -m venv /venv && /venv/bin/python -m pip install --upgrade pip && /venv/bin/pip install -U setuptools

COPY requirements.txt ./
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY arduino-cli-config.py ./

ENTRYPOINT [ "/venv/bin/python", "arduino-cli-config.py" ]
