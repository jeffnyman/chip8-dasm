from chip8_dasm.disassembler import Disassembler
from expects import equal, expect
import pytest


@pytest.fixture
def dasm() -> Disassembler:
    return Disassembler()


def test_no_opcode(dasm: Disassembler) -> None:
    rom_data = [0x99, 0x4E]
    dasm.seed_rom_data(rom_data)
    opcode = dasm.read_opcode()
    operation = dasm.read_operation(opcode)
    address = dasm.read_address(opcode)
    dasm.add_to_disassembly(operation, address)
    # This test is incomplete. It provides full coverage but does not
    # actually provide an expectation.


def test_1nnn(dasm: Disassembler) -> None:
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    dasm.decode()

    expect(dasm.disassembly).to(equal({0x200: "JP lbl_0x024e"}))


def test_6xkk(dasm: Disassembler) -> None:
    rom_data = [0x67, 0x03]
    dasm.seed_rom_data(rom_data)
    dasm.decode()

    expect(dasm.disassembly).to(equal({0x200: "LD V7, 0x03"}))


def test_Annn(dasm: Disassembler) -> None:
    rom_data = [0xA2, 0x02]
    dasm.seed_rom_data(rom_data)
    dasm.decode()

    expect(dasm.disassembly).to(equal({0x200: "LD I, lbl_0x0202"}))
