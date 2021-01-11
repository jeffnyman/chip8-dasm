"""Core disassembly module."""

from typing import Dict, List, Tuple, Union

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
        self.all_contexts: List[int] = []
        self.labels: List[int] = []
        self.current_contexts: List[int] = []
        self.opcodes = {
            0x1000: "JP lbl_0x{:04x}",
            0x6000: "LD V{}, 0x{:02x}",
            0xA000: "LD I, lbl_0x{:04x}",
        }

        if display_insight is True:
            self.insight = Insight()

        if rom_file is not None:
            self.rom_data = Loader.load(rom_file)

        self.current_address = self.STARTING_ADDRESS

    def decode(self, address: int = None) -> None:
        """Process opcodes in ROM file."""

        self.current_address = address if address else self.STARTING_ADDRESS
        context_change = False

        while not context_change:
            if self.current_address - self.STARTING_ADDRESS + 1 > len(self.rom_data):
                self.context_change = True
                break

            print(
                f"Current Address: {self.current_address} ({hex(self.current_address)})"
            )

            opcode = self.read_opcode()
            assert isinstance(opcode, int)

            operation = self.read_operation(opcode)
            assert isinstance(operation, int)

            if self.insight:
                self.insight.execution_context(opcode, operation)

            if operation == 0x1000:
                # 1NNN: Jumps to address NNN.
                # This jump doesn't remember its origin, so no stack interaction
                # is required. However, it is worth having this recognized as a
                # context change with a label.
                context_change = True

                address = self.read_address(opcode)
                assert isinstance(address, int)

                self.add_to_disassembly(operation, address)
                self.add_label(address)
                self.add_context(address)

            elif operation == 0x6000:
                # 6XNN: Sets VX to NN.
                vx = self.read_vx(opcode)
                byte = self.read_byte(opcode)
                self.add_to_disassembly(operation, vx, byte)

            elif operation == 0xA000:
                # ANNN: Sets I to the address NNN.
                address = self.read_address(opcode)
                assert isinstance(address, int)

                self.add_to_disassembly(operation, address)
                self.add_label(address)
            else:
                print("Unknown opcode: 0x{:04x}".format(opcode))
                context_change = True

            self.current_address += 2

            print(f"\nAll Contexts: {self.all_contexts}")
            print(f"Current Contexts: {self.current_contexts}")
            print(f"Labels: {self.labels}\n")

        if len(self.current_contexts) > 0:
            self.decode(self.current_contexts.pop())

    def add_to_disassembly(
        self, operation: int, *args: Union[int, Tuple[int, ...]]
    ) -> None:
        """
        Write disassembly data.

        Information regarding the current address and the operation found at
        that address is written to a data structure.
        """

        try:
            self.disassembly[self.current_address] = self.opcodes[operation].format(
                *args
            )
        except KeyError as key_error:
            click.secho(
                f"\nThe key '{hex(key_error.args[0])}' is not "
                "part of the opcode dictionary.\n",
                fg="red",
                bold=True,
            )

    def add_context(self, address: int) -> None:
        """
        Add an address context to a list of contexts.

        The focus here is that each jump or call to a routine
        """

        if address not in self.all_contexts:
            self.current_contexts.append(address)
            self.all_contexts.append(address)

    def add_label(self, address: int) -> None:
        """
        Add label to the disassembled operation.

        Any operation that leads to a jump or a call, and thus a context
        change, can be provided a label that shows what address is being
        referenced.
        """

        self.labels.append(address)

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

    def read_byte(self, opcode: int) -> int:
        """Read an individual set of 8 bits."""

        # 0xff = 255

        return opcode & 0xFF

    def read_vx(self, opcode: int) -> int:
        """
        Read the value from a register.

        The CHIP-8 has a series of 8-bit registers that arereferred to as Vx
        and Vy, where x or y is a hexadecimal digit.
        """

        if self.insight:
            self.insight.vx(opcode)

        return (opcode & 0xF00) >> 8

    def seed_rom_data(self, rom_data: list) -> None:
        """Seed ROM data.

        This method will take a list of hexadecimal values and convert them
        into a bytearray. This method is only needed as a test hook to allow
        running the unit tests.
        """

        self.rom_data = bytearray(rom_data)
