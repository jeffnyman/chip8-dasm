"""Core disassembly module."""

from typing import Dict

from chip8_dasm.insight import Insight
from chip8_dasm.loader import Loader
import click


class Disassembler:
    """Reads the binary data from a ROM file."""

    STARTING_ADDRESS = 0x200

    def __init__(self, rom_file: str = None, display_insight: bool = False):
        self.rom_file = rom_file
        self.insight = None
        self.disassembly: Dict[int, str] = {}
        self.opcodes = {0x1000: "JP {:04x}"}

        if display_insight is True:
            self.insight = Insight()

        if rom_file is not None:
            self.rom_data = Loader.load(rom_file)

        self.current_address = self.STARTING_ADDRESS

    def decode(self) -> None:
        """Process opcodes in ROM file."""

        while self.current_address - self.STARTING_ADDRESS + 1 < len(self.rom_data):
            print(
                f"Current Address: {self.current_address} ({hex(self.current_address)})"
            )

            opcode = self.read_opcode()
            assert isinstance(opcode, int)

            operation = self.read_operation(opcode)
            assert isinstance(operation, int)

            if operation == 0x1000:
                # 1NNN: Jumps to address NNN.
                # This jump doesn't remember its origin, so no stack interaction
                # is required.
                address = self.read_address(opcode)
                assert isinstance(address, int)

                self.add_to_disassembly(operation, address)
            else:
                print("Unknown opcode: 0x{:04x}".format(opcode))

            self.current_address += 2

        print(self.disassembly)

    def add_to_disassembly(self, operation: int, address: int) -> None:
        """
        Write disassembly data.

        Information regarding the current address and the operation found at
        that address is written to a data structure.
        """

        try:
            self.disassembly[self.current_address] = self.opcodes[operation].format(
                address
            )
        except KeyError as key_error:
            click.secho(
                f"\nThe key '{hex(key_error.args[0])}' is not "
                "part of the opcode dictionary.\n",
                fg="red",
                bold=True,
            )

    def read_opcode(self) -> int:
        """
        Read individual opcode from binary data.

        Each opcode is two bytes and so has to be read in as a word.
        """

        offset = self.current_address - self.STARTING_ADDRESS

        if self.insight:
            self.insight.opcode(self.rom_data, offset)

        return self.rom_data[offset] << 8 | self.rom_data[offset + 1]

    def read_operation(self, opcode: int) -> int:
        """
        Read the upper nibble / msb of an opcode.

        An opocde encodes an operation and relevant data into a number. The
        most significant byte, or upper nibble, contains the operation.
        """

        if self.insight:
            self.insight.operation(opcode)

        return opcode & 0xF000

    def read_address(self, opcode: int) -> int:
        """Read an individual address from the opcode."""

        if self.insight:
            self.insight.address(opcode)

        return opcode & 0xFFF

    def seed_rom_data(self, rom_data: list) -> None:
        """Seed ROM data.

        This method will take a list of hexadecimal values and convert them
        into a bytearray. This method is only needed as a test hook to allow
        running the unit tests.
        """

        self.rom_data = bytearray(rom_data)
