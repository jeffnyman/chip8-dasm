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


def test_decode_address(dasm: Disassembler) -> None:
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    opcode = dasm.read_opcode()
    address = dasm.read_address(opcode)

    expect(hex(address)).to(equal("0x24e"))


def test_unable_to_decode(dasm: Disassembler) -> None:
    rom_data = [0x99, 0x4E]
    dasm.seed_rom_data(rom_data)

    try:
        dasm.decode()
    except IndexError:
        pass
    # This test is incomplete. It provides full coverage but does not
    # actually provide an expectation. The try-except is probably even a
    # greater sin as it's handling the fact that I'm not sure how to design
    # a test that tests this condition but without having the error due to
    # the fact that the current_address is incremented by two for each
    # execution of the decode() call.
