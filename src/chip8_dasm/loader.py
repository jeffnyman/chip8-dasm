"""Loader implementation for CHIP-8 ROM files."""


class Loader:
    """Simple abstraction for a file loader."""

    @staticmethod
    def load(rom_file: str) -> bytearray:
        """Load binary data from ROM file."""

        with open(rom_file, mode="rb") as file:
            return bytearray(file.read())
