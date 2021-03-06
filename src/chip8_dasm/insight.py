"""Insight module for disassembly processing."""

import click


class Insight:
    """Provides insight into disassembly operations."""

    def execution_context(self, opcode: int, operation: int) -> None:
        """Provide context for current decoding operation."""

        click.secho("\n== DECODING ==", fg="green", bold=True)
        click.secho(f"\tOpcode: {hex(opcode)}")
        click.secho(f"\tOperation: {hex(operation)}")

    def opcode(self, data: bytearray, offset: int) -> None:
        """Provide binary breakdown of opcode processing."""

        counter = len(self.binary(data[offset] << 8)[2:])
        tabber = "\t\t" if counter < 16 else "\t"

        click.secho("\nOpcode", fg="cyan", bold=True)

        click.secho(
            f"{self.binary(data[offset])[2:].rjust(counter, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo(f"{tabber}Address offset\n")

        click.secho(
            f"{self.binary(data[offset] << 8)[2:]}", fg="yellow", bold=True, nl=False
        )
        click.echo(f"{tabber}Address offset (shifted 8)")

        click.secho(
            f"{self.binary(data[offset + 1])[2:].rjust(counter, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo(f"{tabber}Address offset (+ 1)")

        click.echo("-" * counter)

        click.secho(
            f"{self.binary(data[offset] << 8 | data[offset + 1])[2:]}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        full_value = data[offset] << 8 | data[offset + 1]

        click.secho(f"{tabber}{full_value} ({hex(full_value)})")

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

    def vx(self, opcode: int) -> None:
        """Provide binary breakdown of register."""

        click.secho("\nvx", fg="cyan", bold=True)

        # 0xf00 = 3840

        click.secho(
            f"{self.binary(opcode)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\topcode")

        click.secho(
            f"{self.binary(0xf00)[2:].rjust(16, ' ')}", fg="yellow", bold=True, nl=False
        )
        click.echo("\t0xF00")

        click.echo("----------------\topcode & 0xF00")

        click.secho(
            f"{self.binary(opcode & 0xf00)[2:].rjust(16, ' ')}\n",
            fg="yellow",
            bold=True,
            nl=False,
        )

        click.echo("----------------\t(opcode & 0xF00) >> 8")

        click.secho(
            f"{self.binary((opcode & 0xf00) >> 8)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        value = (opcode & 0xF00) >> 8

        click.echo(f"\t{value} ({hex(value)})")

    def vy(self, opcode: int) -> None:
        """Provide binary breakdown of register."""

        click.secho("\nvy", fg="cyan", bold=True)

        # 0xf0 = 240

        click.secho(
            f"{self.binary(opcode)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )
        click.echo("\topcode")

        click.secho(
            f"{self.binary(0xf0)[2:].rjust(16, ' ')}", fg="yellow", bold=True, nl=False
        )
        click.echo("\t0xF0")

        click.echo("----------------\topcode & 0xF0")

        click.secho(
            f"{self.binary(opcode & 0xf0)[2:].rjust(16, ' ')}\n",
            fg="yellow",
            bold=True,
            nl=False,
        )

        click.echo("----------------\t(opcode & 0xF0) >> 4")

        click.secho(
            f"{self.binary((opcode & 0xf0) >> 4)[2:].rjust(16, ' ')}",
            fg="yellow",
            bold=True,
            nl=False,
        )

        value = (opcode & 0xF0) >> 4

        click.echo(f"\t{value} ({hex(value)})")

    @staticmethod
    def binary(value: int, length: int = 8) -> str:
        """Convert an integer value into a binary representation."""

        return format(value, "#0{}b".format(length + 2))
