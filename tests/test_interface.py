from click.testing import CliRunner
from expects import equal, expect
import pytest

from chip8_dasm import __version__, cli

@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()

def test_version() -> None:
    expect(__version__).to(equal("0.1.0"))

def test_startup_succeeds(runner: CliRunner) -> None:
    with runner.isolated_filesystem():
        with open('test_rom', 'w'):
            result = runner.invoke(cli.cli, ["test_rom"])

    expect(result.exit_code).to(equal(0))
    expect(result.output).to(equal("ROM File: test_rom\n"))
