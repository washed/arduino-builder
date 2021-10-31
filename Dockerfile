FROM python:3.9-slim-buster

WORKDIR /usr/src/app

RUN apt-get clean && apt-get update && apt-get upgrade -y
RUN apt-get install curl wget sudo gpg lsb-release software-properties-common -y
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/0.19.3/install.sh | sh

# Install clang-format 13 (default repos carry clang-format form the stone ages)
RUN sudo wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN sudo add-apt-repository "deb http://apt.llvm.org/buster/   llvm-toolchain-buster-13  main"
RUN apt-get update
RUN apt-get install clang-format-13 -y
RUN ln /usr/bin/clang-format-13 /usr/bin/clang-format

RUN python -m venv /venv && /venv/bin/python -m pip install --upgrade pip && /venv/bin/pip install -U setuptools

COPY requirements.txt ./
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY arduino-cli-config.py ./

ENTRYPOINT [ "/venv/bin/python", "arduino-cli-config.py" ]
