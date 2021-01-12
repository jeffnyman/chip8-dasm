"""Writer implementation for CHIP-8 ROM disassemebly."""

from typing import Tuple

from chip8_dasm.disassembler import Disassembler


class Writer:
    """Simple abstraction for a disassembly writer."""

    STARTING_ADDRESS = 0x200

    def __init__(self, dasm: Disassembler):
        self.dasm = dasm

    def generate(self) -> None:
        """Write out disassembly information."""

        dasm_output = self.generate_disassembly_buffer(self.STARTING_ADDRESS)

        print(dasm_output)

    def generate_disassembly_buffer(self, address: int) -> str:
        """Create buffer structure for disassembly data."""

        dasm_buffer = "start:\n"

        while address < self.end_rom_file():
            line, address = self.generate_instructions(address)
            dasm_buffer += line

        return dasm_buffer

    def generate_instructions(self, address: int) -> Tuple[str, int]:
        """Iterate through all instructions for the disassembly buffer."""

        line = ""

        if address in self.dasm.disassembly:
            line = "     {}\n".format(self.dasm.disassembly[address])
            address += 2
        else:
            address += 1

        return (line, address)

    def end_rom_file(self) -> int:
        """Return the length of the non-interpreter portion of ROM."""

        return self.STARTING_ADDRESS + len(self.dasm.rom_data)
