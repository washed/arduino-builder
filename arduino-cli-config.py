import logging
from os import getenv
from subprocess import check_output
from typing import List, Optional

import click
import yaml
from pydantic import BaseModel, HttpUrl

logging.basicConfig()
LOGGER = logging.getLogger()
LOGGER.setLevel("DEBUG")


DEFAULT_CLI_DIR = "/usr/src/app/bin"
DEFAULT_CLI_CMD = f"{DEFAULT_CLI_DIR}/arduino-cli"
CONFIG_FILE_NAME = getenv("CONFIG_FILE_NAME", "arduino-builder-config.yml")
BUILD_DIR = "/usr/src/app/build"
BUILD_CACHE_DIR = "/usr/src/app/build_cache"


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


def call(commands: List[str]):
    LOGGER.info("Calling '%s'", " ".join(commands))
    return check_output(commands, encoding="utf-8")


def config_init(cmd):
    call([cmd, "config", "init", "--overwrite"])


def update_index(cmd):
    call([cmd, "core", "update-index"])


def update(cmd):
    call([cmd, "update"])


def upgrade(cmd):
    call([cmd, "upgrade"])


def build(cmd, compile: ArduinoBuilderCompileConfig):
    compile_cmd = [cmd, "compile", "--warnings", compile.warnings]
    if compile.verbose:
        compile_cmd.append("-v")
    compile_cmd.extend(["--build-path", BUILD_DIR, "--build-cache-path",
                       BUILD_CACHE_DIR, "-b", compile.board_type, compile.project_dir])
    output = call(compile_cmd)
    LOGGER.info(output)


def install_libs(cmd, libs: List[str]):
    for lib in libs:
        LOGGER.info("Installing lib: %s", lib)
        try:
            call([cmd, "lib", "install", lib])
        except Exception as exc:
            LOGGER.exception(exc)


def install_boards(cmd, boards: List[str]):
    for board in boards:
        LOGGER.info("Installing board: %s", board)
        try:
            call([cmd, "core", "install", board])
        except Exception as exc:
            LOGGER.exception(exc)


def add_urls(cmd, urls: List[HttpUrl]):
    for url in urls:
        LOGGER.info("Adding URL: %s", url)
        call([cmd, "config", "add", "board_manager.additional_urls", url])


@click.command()
@click.option("--arduino-cli", default=DEFAULT_CLI_CMD)
@click.option("--compile/--no-compile", default=True)
@click.option("--init/--no-init", default=True)
def main(arduino_cli, compile, init):
    with open(CONFIG_FILE_NAME, "r") as file:
        try:
            config_yaml = yaml.safe_load(file)
            config = ArduinoBuilderConfig(**config_yaml)
            LOGGER.info(config)
        except yaml.YAMLError as exc:
            LOGGER.exception(exc)
            return

    if init:
        config_init(arduino_cli)
        add_urls(arduino_cli, config.additional_board_urls)
        update_index(arduino_cli)
        update(arduino_cli)
        upgrade(arduino_cli)
        install_libs(arduino_cli, config.libraries)
        install_boards(arduino_cli, config.boards)

    if config.compile and compile:
        build(arduino_cli, config.compile)


if __name__ == "__main__":
    main()
