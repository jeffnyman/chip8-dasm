from chip8_dasm.disassembler import Disassembler
from expects import equal, expect
import pytest


@pytest.fixture
def dasm() -> Disassembler:
    return Disassembler()


def test_decode(dasm: Disassembler) -> None:
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    value = dasm.read_opcode()

    expect(hex(value)).to(equal("0x124e"))
