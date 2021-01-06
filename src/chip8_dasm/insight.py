"""Insight module for disassembly processing."""

import click


class Insight:
    """Provides insight into disassembly operations."""

    def opcode(self, data: bytearray, offset: int) -> None:
        """Provide binary breakdown of opcode processing."""

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

        click.secho(f"\t= {full_value} ({hex(full_value)})")

    @staticmethod
    def binary(value: int, length: int = 8) -> str:
        """Convert an integer value into a binary representation."""

        return format(value, "#0{}b".format(length + 2))
