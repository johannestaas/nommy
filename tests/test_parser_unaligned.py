import pytest

from nommy import parser, le_u, le_i


@parser
class LEData:
    u8: le_u(8)
    # 1 byte
    u4: le_u(4)
    u3: le_u(3)
    u1: le_u(1)
    # 2 byte
    u2_1: le_u(2)
    u2_2: le_u(2)
    i2_1: le_i(2)
    i2_2: le_i(2)
    # 3 byte
    i8_1: le_i(8)
    # 4 byte
    i8_2: le_i(8)
    # 5 byte
    i16: le_i(16)
    # 7 byte
    i4: le_i(4)
    i3: le_i(3)
    u1_2: le_u(1)
    # 8 byte


@pytest.mark.skip
def test_ledata_ff():
    data, rest = LEData.parse(b'\xff' * 8)
    assert data.u8 == 0xff
    assert data.u4 == 0b1111
    assert data.u3 == 0b111
    assert data.u1 == 0b1
    assert data.u2_1 == 0b11
    assert data.u2_2 == 0b11
    assert data.i2_1 == -0b01
    assert data.i2_2 == -0b01
    assert data.i8_1 == -0b01111111
    assert data.i8_2 == -0b01111111
    assert data.i16 == -0x7fff
    assert data.i4 == -0b0111
    assert data.i3 == -0b011
    assert data.u1_2 == 0b1
    assert rest == b''


@parser
class LESimple:
    u8_1: le_u(8)
    # 1 byte
    u4_1: le_u(4)
    u4_2: le_u(4)
    # 2 byte
    u3_1: le_u(3)
    u1_1: le_u(1)
    u3_2: le_u(3)
    u1_2: le_u(1)
    # 3 byte
    u5_1: le_u(5)
    u3_3: le_u(3)
    # 4 byte
    u16_1: le_u(16)
    # 6 byte


def test_lesimple_ff():
    data, rest = LESimple.parse(b'\xff' * 8)
    assert data == LESimple(
        u8_1=0xff,
        u4_1=0x0f,
        u4_2=0x0f,
        u3_1=0x07,
        u1_1=0x01,
        u3_2=0x07,
        u1_2=0x01,
        u5_1=0x1f,
        u3_3=0x07,
        u16_1=0xffff,
    )
    assert rest == b'\xff\xff'
