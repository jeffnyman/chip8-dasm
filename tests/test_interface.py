import os
import os.path as path
from typing import Generator

from chip8_dasm import __version__, cli
from click.testing import CliRunner
from expects import contain, equal, expect
import pytest


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


def rom_example() -> str:
    file_path = path.join(path.dirname(__file__), "./fixtures", "test_opcode.ch8")
    return file_path


@pytest.fixture
def rom() -> Generator:
    yield rom_example()


def test_startup_succeeds(runner: CliRunner, rom: str) -> None:
    rom_name = os.path.basename(rom)
    result = runner.invoke(cli.cli, [rom])

    expect(result.exit_code).to(equal(0))
    expect(result.output).to(contain(f"ROM File: {rom_name}\n"))


def test_version() -> None:
    expect(__version__).to(equal("0.1.0"))
