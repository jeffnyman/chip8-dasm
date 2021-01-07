from chip8_dasm.disassembler import Disassembler
from expects import equal, expect
import pytest


@pytest.fixture
def dasm() -> Disassembler:
    return Disassembler()


def test_no_opcode(dasm):
    rom_data = [0x99, 0x4E]
    dasm.seed_rom_data(rom_data)
    opcode = dasm.read_opcode()
    operation = dasm.read_operation(opcode)
    address = dasm.read_address(opcode)
    dasm.add_to_disassembly(operation, address)
    # This test is incomplete. It provides full coverage but does not
    # actually provide an expectation.


def test_1nnn(dasm):
    rom_data = [0x12, 0x4E]
    dasm.seed_rom_data(rom_data)
    dasm.decode()

    expect(dasm.disassembly).to(equal({
        0x200: 'JP 024e'
    }))
