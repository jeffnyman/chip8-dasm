import click

from chip8_dasm import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.argument("rom_file", type=click.Path(exists=True))
def cli(rom_file: str) -> None:
    """Disassemble ROM_FILE.

    ROM_FILE is the rom binary file to load.
    """

    click.echo("ROM File: ", nl=False)
    click.secho(f"{rom_file}", fg="green", bold=True)

    pass

def main() -> None:
    """Entry point for the disassembler."""

    print("\nCHIP-8 Disassembler\n")

    cli(prog_name="c8dasm")