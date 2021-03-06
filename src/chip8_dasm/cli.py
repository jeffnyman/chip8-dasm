"""Command line interface module for the disassembler."""

import os

from chip8_dasm import __version__
from chip8_dasm.disassembler import Disassembler
from chip8_dasm.writer import Writer
import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.argument("rom_file", type=click.Path(exists=True))
@click.option("-i", "--insight", is_flag=True, help="execution details")
def cli(rom_file: str, insight: bool) -> None:
    """Disassemble ROM_FILE.

    ROM_FILE is the rom binary file to load.
    """

    click.echo("ROM File: ", nl=False)
    click.secho(f"{os.path.basename(rom_file)}", fg="green", bold=True)

    dasm = Disassembler(rom_file, insight)
    assert isinstance(dasm.rom_data, bytearray)

    dasm.decode()

    writer = Writer(dasm)
    writer.generate()


def main() -> None:
    """Entry point for the disassembler."""

    print("\nCHIP-8 Disassembler\n")

    cli(prog_name="c8dasm")
