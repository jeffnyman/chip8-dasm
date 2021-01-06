"""Insight module for disassembly processing."""

import click


class Insight:
    """Provides insight into disassembly operations."""

    def opcode(self, data: bytearray, offset: int) -> None:
        """Provide binary breakdown of opcode processing."""

        click.secho("\nOpcode", fg="cyan", bold=True)

        click.secho(
            f"{self.binary(data[offset])[2:].rjust(13, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\tAddress offset\n")

        click.secho(
            f"{self.binary(data[offset] << 8)[2:]}", fg="yellow", bold=True, nl=False
        )
        click.echo("\tAddress offset (shifted 8)")

        click.secho(
            f"{self.binary(data[offset + 1])[2:].rjust(13, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\tAddress offset (+ 1)")

        click.echo("-------------")

        click.secho(
            f"{self.binary(data[offset] << 8 | data[offset + 1])[2:]}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        full_value = data[offset] << 8 | data[offset + 1]

        click.secho(f"\t{full_value} ({hex(full_value)})")

    def operation(self, opcode: int) -> None:
        """Provide binary breakdown of operation bits from opcode."""

        click.secho("\nOperation", fg="cyan", bold=True)

        click.secho(
            f"{self.binary(opcode)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\topcode")

        click.secho(f"{self.binary(0xf000)[2:]}", fg="yellow", bold=True, nl=False)
        click.echo("\t0xF000")

        click.echo("----------------\topcode & 0xF000")

        click.secho(
            f"{self.binary(opcode & 0xf000)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        value = opcode & 0xF000

        click.echo(f"\t{value} ({hex(value)})")

    def address(self, opcode: int) -> None:
        """Provide binary breakdown of address from opcode."""

        click.secho("\nAddress", fg="cyan", bold=True)

        # 0xfff = 4095

        click.secho(
            f"{self.binary(opcode)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\topcode")

        click.secho(
            f"{self.binary(0xfff)[2:].rjust(16, ' ')}", fg="yellow", bold=True, nl=False
        )
        click.echo("\t0xFFF")

        click.echo("----------------\topcode & 0xFFF")

        click.secho(
            f"{self.binary(opcode & 0xfff)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        value = opcode & 0xFFF

        click.echo(f"\t{value} ({hex(value)})")

    @staticmethod
    def binary(value: int, length: int = 8) -> str:
        """Convert an integer value into a binary representation."""

        return format(value, "#0{}b".format(length + 2))
