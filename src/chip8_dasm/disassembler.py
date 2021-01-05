"""Core disassembly module."""

from chip8_dasm.loader import Loader


class Disassembler:
    """Reads the binary data from a ROM file."""

    def __init__(self, rom_file: str):
        self.rom_file = rom_file
        self.rom_data = Loader.load(rom_file)
