import logging
from os import getenv
from subprocess import STDOUT, CalledProcessError, check_output
from typing import List, Optional

import yaml
from pydantic import BaseModel, HttpUrl

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel("DEBUG")


CLI_CMD = "arduino-cli"
CONFIG_FILE_NAME = getenv("CONFIG_FILE_NAME", "arduino-builder-config.yml")
CONFIG_EXISTS_MSG = "Config file already exists, use --overwrite to discard the existing one."


class ArduinoBuilderCompileConfig(BaseModel):
  verbose: bool = True
  warnings: str = "more"
  board_type: str
  project_dir: str


class ArduinoBuilderConfig(BaseModel):
    additional_board_urls: Optional[List[HttpUrl]]
    boards: Optional[List[str]]
    libraries: Optional[List[str]]
    compile: Optional[ArduinoBuilderCompileConfig]


def call(commands: List[str], ignored_errors: List[str] = []):
    try:
        check_output(commands, stderr=STDOUT, encoding="utf-8")
    except CalledProcessError as exc:
        LOGGER.debug("EXC: %s", exc.output)
        if any(ignored_error in exc.output for ignored_error in ignored_errors):
            return
        raise


def config_init():
    call([CLI_CMD, "config", "init", "--overwrite"], [CONFIG_EXISTS_MSG])


def update_index():
    call([CLI_CMD, "core", "update-index"])


def update():
    call([CLI_CMD, "update"])


def upgrade():
    call([CLI_CMD, "upgrade"])


def compile(compile: ArduinoBuilderCompileConfig):
    if compile is None:
        return

    compile_cmd = [CLI_CMD, "compile", "--warnings", compile.warnings]
    if compile.verbose:
        compile_cmd.append("-v")
    compile_cmd.extend([f"-b {compile.board_type}", compile.project_dir])
    call(compile_cmd)


def install_libs(libs: List[str]):
    for lib in libs:
        LOGGER.info("Installing lib: %s", lib)
        try:
            call([CLI_CMD, "lib", "install", lib])
        except Exception as exc:
            LOGGER.exception(exc)


def install_boards(boards: List[str]):
    for board in boards:
        LOGGER.info("Installing board: %s", board)
        try:
            call([CLI_CMD, "core", "install", board])
        except Exception as exc:
            LOGGER.exception(exc)


def add_urls(urls: List[HttpUrl]):
    for url in urls:
        LOGGER.info("Adding URL: %s", url)
        call([CLI_CMD, "config", "add", "board_manager.additional_urls", url])


def main():
    with open(CONFIG_FILE_NAME, "r") as file:
        try:
            config_yaml = yaml.safe_load(file)
            config = ArduinoBuilderConfig(**config_yaml)
            LOGGER.info(config)
        except yaml.YAMLError as exc:
            LOGGER.exception(exc)
            return

    config_init()
    add_urls(config.additional_board_urls)
    update_index()
    update()
    upgrade()
    install_libs(config.libraries)
    install_boards(config.boards)
    compile(config.compile)


if __name__ == "__main__":
    main()
