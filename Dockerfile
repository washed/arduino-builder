FROM python:3.9-slim-buster

RUN apt-get clean && apt-get update
# && apt-get upgrade -y
RUN apt-get install curl clang-format sudo -y
RUN curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/0.19.3/install.sh | BINDIR=/usr/bin sh

# RUN arduino-cli config init
# RUN arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/washed/CO2-Ampel/master/package_co2ampel_index.json
# RUN arduino-cli core update-index
# RUN arduino-cli update
# RUN arduino-cli upgrade
# RUN arduino-cli lib install ArduinoJson
# RUN arduino-cli core install arduino:samd
# RUN arduino-cli core install co2ampel:samd

# RUN useradd --create-home --shell /bin/bash runner
# USER runner
# WORKDIR /home/runner
# 
# RUN arduino-cli config init
# RUN arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/washed/CO2-Ampel/master/package_co2ampel_index.json
# RUN arduino-cli core update-index
# RUN arduino-cli update
# RUN arduino-cli upgrade
# RUN arduino-cli lib install ArduinoJson
# RUN arduino-cli core install arduino:samd
# RUN arduino-cli core install co2ampel:samd
