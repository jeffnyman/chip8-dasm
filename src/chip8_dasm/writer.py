"""Writer implementation for CHIP-8 ROM disassemebly."""

from chip8_dasm.disassembler import Disassembler


class Writer:
    """Simple abstraction for a disassembly writer."""

    def __init__(self, dasm: Disassembler):
        self.dasm = dasm

    def generate(self) -> None:
        """Write out disassembly information."""

        print(self.dasm.disassembly)
