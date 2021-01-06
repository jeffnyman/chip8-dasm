from chip8_dasm.disassembler import Disassembler
from expects import equal, expect
import pytest


@pytest.fixture
def dasm() -> Disassembler:
    return Disassembler()


def test_decode_opcode(dasm: Disassembler) -> None:
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    opcode = dasm.read_opcode()

    expect(hex(opcode)).to(equal("0x124e"))


def test_decode_operation(dasm: Disassembler) -> None:
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    opcode = dasm.read_opcode()
    operation = dasm.read_operation(opcode)

    expect(hex(operation)).to(equal("0x1000"))
